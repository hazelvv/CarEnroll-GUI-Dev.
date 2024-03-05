import tkinter as tk
from tkinter import ttk, messagebox
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir="/Users/rebecca/Downloads/instantclient_19_16")

class EmpManApp:
    # 클래스 레벨에서 데이터베이스 연결 설정
    username = "system"
    password = "oracle"
    dsn = "localhost:1521/xe"
    connection = cx_Oracle.connect(username, password, dsn)
    
    def __init__(self, master):
        self.master = master
        self.master.title("carenroll system")
        self.master.geometry("600x500")

        # Create a style for the tab control
        style = ttk.Style()
        style.configure("CustomTab.TNotebook.Tab", foreground="black", font=("Helvetica", 30))

        # Create a tab control
        self.notebook = ttk.Notebook(master)

        self.notebook.pack(expand=True, fill=tk.BOTH)
       
        # 차량 조회 페이지
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="차량 조회")
        self.setup_search_page(self.search_frame)
        
        # 차량 등록 페이지
        self.register_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.register_frame, text="차량 등록")
        self.setup_register_page(self.register_frame)

       

    def setup_search_page(self, frame):
        # 차량 조회 페이지 설정

         # 차량 조회 텍스트
        self.search_label = tk.Label(frame, text="번호입력")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)

        # 차량 번호 입력
        self.search_entry = tk.Entry(frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        # 검색 버튼
        self.search_button = tk.Button(frame, text="차량검색", command=self.search_by_carnum)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        # 조회 결과 텍스트 박스
        self.search_result_text = tk.Text(frame, height=10, width=70)
        self.search_result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    def setup_register_page(self, frame):
        # 차량 등록 페이지 설정
        # 소유자, 차량번호, 모델명, 전화번호, 주소 입력
        fields = ["소유자", "차량번호", "모델명", "전화번호", "주소"]
        self.register_entries = {}
        for i, field in enumerate(fields):
            label = tk.Label(frame, text=field)
            label.grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.register_entries[field] = entry

        # 저장 버튼
        self.save_button = tk.Button(frame, text="차량등록", command=self.register_car)
        self.save_button.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=10)

    def register_car(self):
        # 차량 등록 함수
        fields = ["소유자", "차량번호", "모델명", "전화번호", "주소"]
        values = [self.register_entries[field].get() for field in fields]

        try:
            cursor = self.connection.cursor()
            
            # 차량 등록 SQL 쿼리 실행
            sql_query = f"INSERT INTO ENROLLEDCAR ({', '.join(fields)}) VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}')"

            cursor.execute(sql_query)
            self.connection.commit()  # 변경 사항을 커밋

            # 등록 완료 메시지 표시
            messagebox.showinfo("등록 완료", "차량이 성공적으로 등록되었습니다.")
            
            # 커서 닫기
            cursor.close()
        except cx_Oracle.Error as error:
            messagebox.showerror("오류", f"차량 등록 중 오류 발생: {error}")

    def search_by_carnum(self):
        # 차량 조회 함수
        carnum = self.search_entry.get()
        
        try:
            cursor = self.connection.cursor()
            
            # 차량번호로 소유자 정보 검색
            sql_query = f"SELECT NAME, CARNUM, MODEL, PHONE, ADDRESS FROM ENROLLEDCAR WHERE CARNUM LIKE '%{carnum}%'"
            cursor.execute(sql_query)
            
            # 결과 가져오기
            row = cursor.fetchone()  # 하나의 행만 가져옴
            
            if row:
                # 결과 출력
                owner_name, carnum, model, phone, address = row
                
                # 출력 형식에 맞게 텍스트 박스에 설정
                self.search_result_text.delete(1.0, tk.END)
                self.search_result_text.insert(tk.END, f"소유자: {owner_name}\n")
                self.search_result_text.insert(tk.END, f"차량번호: {carnum}\n")
                self.search_result_text.insert(tk.END, f"차량번호: {model}\n")
                self.search_result_text.insert(tk.END, f"전화번호: {phone}\n")
                self.search_result_text.insert(tk.END, f"주소: {address}\n")
            else:
                # 검색된 결과가 없는 경우 메시지 출력
                messagebox.showinfo("검색 결과", "해당하는 차량번호의 정보가 없습니다.")
            
            # 커서 닫기
            cursor.close()
        except cx_Oracle.Error as error:
            messagebox.showerror("오류", f"Oracle 데이터베이스 연결 중 오류 발생: {error}")


def main():
    root = tk.Tk()
    app = EmpManApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
