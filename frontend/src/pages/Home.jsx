import React from 'react'
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'

const data = [{name:'Open', value: 12},{name:'Closed', value: 28},{name:'Overdue', value:5}]
const COLORS = ['#0088FE', '#00C49F', '#FF8042']

export default function Home(){
  return (
    <div style={{padding:20}}>
      <header style={{display:'flex', alignItems:'center', gap:12}}>
        <img src='/public/logo.svg' alt='logo' style={{height:56}} />
        <h2 style={{margin:0}}>FAT-EIBL</h2>
      </header>
      <hr />
      <div style={{display:'flex', gap:20}}>
        <div style={{width:360}}>
          <h3>Compliance Overview</h3>
          <PieChart width={300} height={250}><Pie data={data} dataKey='value' nameKey='name' cx='50%' cy='50%' outerRadius={80}>{data.map((entry,index)=>(<Cell key={'cell-'+index} fill={COLORS[index % COLORS.length]} />))}</Pie><Tooltip /><Legend /></PieChart>
        </div>
        <div style={{flex:1}}>
          <h3>Quick Actions</h3>
          <ul>
            <li>Create Audit Request</li>
            <li>Import Excel</li>
            <li>View Audit Logs</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
