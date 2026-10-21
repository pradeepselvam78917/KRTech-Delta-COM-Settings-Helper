import tkinter as tk
from tkinter import ttk, messagebox

# Conservative D1120 encoder. Only verified example profile is enabled.
BAUD_CODES = {4800:0x70,9600:0x80,19200:0x90,38400:0xA0,57600:0xB0,115200:0xC0}

root=tk.Tk(); root.title('KRTech Delta DVP12SA2 COM Helper'); root.geometry('780x650'); root.minsize(680,560)
main=ttk.Frame(root,padding=18);main.pack(fill='both',expand=True)
ttk.Label(main,text='Delta DVP12SA2 — Communication Settings Helper',font=('Segoe UI',16,'bold')).pack(anchor='w')
ttk.Label(main,text='Offline calculator only — does not connect to or change the PLC.',foreground='#555').pack(anchor='w',pady=(3,16))
controls=ttk.Frame(main);controls.pack(fill='x')
fields=[('Port',['COM1 (RS232)','COM2 (RS485)','COM3 (RS485)'],'COM2 (RS485)'),('Baud rate',[str(x) for x in BAUD_CODES],'57600'),('Data bits',['7','8'],'8'),('Parity',['None','Even','Odd'],'Even'),('Stop bits',['1','2'],'1'),('Protocol',['Modbus RTU','Modbus ASCII'],'Modbus RTU'),('Slave ID',[str(x) for x in range(1,248)],'1')]
vars={}
for i,(label,choices,default) in enumerate(fields):
    ttk.Label(controls,text=label).grid(row=i,column=0,sticky='w',pady=5)
    var=tk.StringVar(value=default);vars[label]=var
    box=ttk.Combobox(controls,textvariable=var,values=choices,state='readonly',width=28)
    box.grid(row=i,column=1,sticky='w',padx=12,pady=5)
output=tk.Text(main,height=15,wrap='word',font=('Consolas',10),state='disabled')
output.pack(fill='both',expand=True,pady=(14,8))

def calculate(*_):
    port=vars['Port'].get();baud=int(vars['Baud rate'].get());bits=vars['Data bits'].get();parity=vars['Parity'].get();stop=vars['Stop bits'].get();proto=vars['Protocol'].get();slave=vars['Slave ID'].get()
    lines=['SELECTED SETTINGS',f'Port: {port}',f'Serial: {baud}, {bits}{parity[0] if parity!="None" else "N"}{stop}',f'Protocol: {proto}',f'Slave ID: {slave}','']
    if port.startswith('COM2') and bits=='8' and parity=='Even' and stop=='1' and proto=='Modbus RTU':
        value=BAUD_CODES[baud]|0x07
        lines += ['COM2 — D1120 example profile (8E1):',f'Hexadecimal: H{value:02X}',f'Decimal: K{value}', '', 'WPLSoft instruction text (review before use):', 'LD M1002',f'MOV H{value:02X} D1120',f'MOV K{slave} D1121','SET M1120','SET M1143','', 'ESP32 serial:',f'Serial2.begin({baud}, SERIAL_8E1, 16, 17);']
    else:
        lines += ['NOT VERIFIED FOR THIS COMBINATION','No PLC register value is generated.', 'COM1/COM3 use port-specific settings.','Other framing and ASCII profiles require the exact Delta manual encoding.','Do not reuse COM2 D1120 values for other ports.']
    lines += ['', 'CAUTION: Check PLC firmware, port availability and existing ladder logic.', 'Back up the PLC program and change communication only with machine safely stopped.', 'Values are offline suggestions, not live PLC readback.']
    output.configure(state='normal');output.delete('1.0','end');output.insert('1.0','\n'.join(lines));output.configure(state='disabled')
for v in vars.values():v.trace_add('write',calculate)
ttk.Button(main,text='Calculate / Refresh',command=calculate).pack(anchor='e')
calculate();root.mainloop()
