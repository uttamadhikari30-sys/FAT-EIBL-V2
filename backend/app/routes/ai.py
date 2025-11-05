from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import os, logging
import openai
from ..auth_utils import get_current_user
from ..audit import record_audit

router = APIRouter(prefix='/ai', tags=['ai'])

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY
else:
    logging.warning('OPENAI_API_KEY not set; AI disabled')

class ChatMessage(BaseModel):
    messages: list[dict]

@router.post('/chat')
async def chat_ai(payload: ChatMessage, user = Depends(get_current_user)):
    if not OPENAI_KEY:
        raise HTTPException(status_code=503, detail='AI not configured')
    if len(payload.messages) > 30:
        raise HTTPException(status_code=400, detail='Too many messages')
    total_len = sum(len(m.get('content','')) for m in payload.messages)
    if total_len > 20000:
        raise HTTPException(status_code=400, detail='Message too long')
    body = {
        'model': OPENAI_MODEL,
        'messages': payload.messages,
        'temperature': float(os.getenv('OPENAI_TEMPERATURE', 0.2)),
        'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', 800)) if os.getenv('OPENAI_MAX_TOKENS') else 800,
    }
    try:
        resp = openai.ChatCompletion.create(**body)
        assistant_msg = resp['choices'][0]['message']['content']
        record_audit(actor=getattr(user,'username','unknown'), action='AI_QUERY', resource='AI_CHAT', summary=(assistant_msg[:200] if assistant_msg else ''), payload={'prompt_len': total_len})
        return {'reply': assistant_msg, 'usage': resp.get('usage')}
    except openai.error.OpenAIError as e:
        logging.exception('OpenAI error')
        raise HTTPException(status_code=502, detail=f'AI service error: {str(e)}')
    except Exception as e:
        logging.exception('Unexpected error')
        raise HTTPException(status_code=500, detail='AI internal error')
