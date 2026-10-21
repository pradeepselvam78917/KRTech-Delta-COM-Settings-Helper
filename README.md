# KRTech Delta DVP12SA2 COM Settings Helper

Run on Windows with Python 3:

```powershell
py delta_com_helper.py
```

Uses built-in tkinter. No pip packages needed.

This is an **offline configuration helper**, not a PLC programming tool.
Only COM2 Modbus RTU 8E1 is encoded using the example D1120 Hx7 values.
Other combinations intentionally show "not verified" instead of inventing register values.

Before changing your PLC: back up the ladder, verify the model-specific Delta manual, and check existing COM2 ladder configuration. COM1 and COM3 require separate register tables and may not support all selections.
