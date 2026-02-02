# AI Circuit Fault Detector
This project detects faulty electronic circuits using simulation data (CSV).
## Features
- Upload circuit CSV data
- Works even if some parameters are missing
- Signal analysis (RMS, attenuation)
- Fault prediction with confidence score
- FastAPI backend
- Ready for deployment
## Tech Stack
- Python
- FastAPI
- NumPy
- Pandas
- Signal Processing
## How to run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
