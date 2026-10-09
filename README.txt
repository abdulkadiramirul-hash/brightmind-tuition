# BrightMind Tuition Centre Mini Project

## Files
- `student_module.py`: functions, `Student` and `PremiumStudent` classes, inheritance and magic methods.
- `main.py`: Streamlit GUI, exception handling, subject fee calculation, NumPy/Pandas analysis and Matplotlib graph.

## Run locally
1. Install Python 3.
2. Open Command Prompt in this folder.
3. Install packages:
   `pip install streamlit numpy pandas matplotlib`
4. Run:
   `streamlit run main.py`

## Streamlit Community Cloud
Upload both Python files to the same GitHub repository, then deploy `main.py` as the app entry point.

## Notes
- Regular student fee = sum of selected subject fees.
- Premium student receives a 10% subject-fee discount.
- The `__add__` magic method adds the marks of two Student objects.
- `calculate_fee()` demonstrates flexible calls with default parameters, the Python approach commonly used to demonstrate function-overloading-style behaviour.
