**Muc tieu**
Mot lenh o may local de day code, mot lenh o PythonAnywhere de cap nhat va reload.

**File da tao**
- `deploy.ps1`
- `update_pythonanywhere.sh`
- `.gitignore`

**1. Khoi tao git neu project chua san sang**
Chay trong thu muc project:

```powershell
cd C:\Users\ngo.van.thien\Documents\attendance_system_lyhoa\attendance_system
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/thiennv57/attendance_system_lyhoa.git
git push -u origin main
```

**2. Clone len PythonAnywhere**

```bash
git clone https://github.com/thiennv57/attendance_system_lyhoa.git ~/attendance_system_lyhoa
cd ~/attendance_system_lyhoa
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x update_pythonanywhere.sh
```

**3. Cau hinh reload file tren PythonAnywhere**
Tim file WSGI trong tab Web, vi du:

```bash
export RELOAD_FILE=/var/www/yourusername_pythonanywhere_com_wsgi.py
export PROJECT_DIR=$HOME/attendance_system_lyhoa
```

Neu muon luu co dinh, them vao `~/.bashrc`.

**4. Cach dung hang ngay**
O may local:

```powershell
.\deploy.ps1 "fix giao dien test"
```

Tren PythonAnywhere:

```bash
cd ~/attendance_system_lyhoa
./update_pythonanywhere.sh
```

**5. Cach lam dung la "mot lenh"**
- Local: `.\deploy.ps1 "noi dung cap nhat"`
- PythonAnywhere: `./update_pythonanywhere.sh`

**6. Luu y**
- Khong dua `instance/*.db`, `uploads/`, `backups/`, `venv/` len git.
- SQLite tren PythonAnywhere nen duoc backup rieng, khong dong bo bang git.
- Neu ban thay doi thu vien, script server se tu `pip install -r requirements.txt`.
