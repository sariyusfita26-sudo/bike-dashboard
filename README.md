# Dashboard Penyewaan Sepeda 2011-2012 🚴

Dashboard ini menampilkan analisis penyewaan sepeda harian dan per jam selama tahun 2011-2012.  
Dibuat menggunakan **Python 3.14.2**, **Streamlit**, **Pandas**, **NumPy**, **Matplotlib**, dan **Seaborn**.

---

## 1. Persiapan Environment

### Python Virtual Environment
Buka terminal di folder proyek, lalu jalankan perintah berikut:

```powershell
cd submission
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate
pip install -r requirements.txt

```
## 2. Jalankan Dashboard

```powershell
cd dashboard
streamlit run dashboard.py
