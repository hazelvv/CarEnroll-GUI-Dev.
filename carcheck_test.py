import tkinter as tk
from tkinter import messagebox
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
        self.master.geometry("800x800")
        
        # 차량 조회 텍스트
        self.search_label = tk.Label(master, text="차량 조회")
        self.search_label.grid(row=0, column=0, padx=10, pady=10)

        # 차량 번호 검색 엔트리
        self.search_entry = tk.Entry(master)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        # 차량 조회 버튼
        self.search_button = tk.Button(master, text="차량 조회", command=self.search_by_carnum)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        # 차량 조회 결과 텍스트 박스
        self.search_result_label = tk.Label(master, text="차량 조회 결과:")
        self.search_result_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.search_result_text = tk.Text(master, height=5, width=50)
        self.search_result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W)

        # 차량 등록 버튼
        self.register_label = tk.Label(master, text="차량 등록")
        self.register_label.grid(row=3, column=0, padx=10, pady=10)

        # 소유자 레이블과 엔트리
        self.owner_label = tk.Label(master, text="소유자:")
        self.owner_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.owner_entry = tk.Entry(master)
        self.owner_entry.grid(row=4, column=1, padx=10, pady=10)

        # 차량번호 레이블과 엔트리
        self.carnum_label = tk.Label(master, text="차량번호:")
        self.carnum_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        self.carnum_entry = tk.Entry(master)
        self.carnum_entry.grid(row=5, column=1, padx=10, pady=10)

        # 모델명 레이블과 엔트리
        self.model_label = tk.Label(master, text="모델명:")
        self.model_label.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
        self.model_entry = tk.Entry(master)
        self.model_entry.grid(row=6, column=1, padx=10, pady=10)

        # 전화번호 레이블과 엔트리
        self.phone_label = tk.Label(master, text="전화번호:")
        self.phone_label.grid(row=7, column=0, padx=10, pady=10, sticky=tk.W)
        self.phone_entry = tk.Entry(master)
        self.phone_entry.grid(row=7, column=1, padx=10, pady=10)

        # 주소 레이블과 엔트리
        self.address_label = tk.Label(master, text="주소:")
        self.address_label.grid(row=8, column=0, padx=10, pady=10, sticky=tk.W)
        self.address_entry = tk.Entry(master)
        self.address_entry.grid(row=8, column=1, padx=10, pady=10)
         # 차량 등록 버튼
        self.register_button = tk.Button(master, text="차량 등록", command=self.register_car)
        self.register_button.grid(row=9, column=0, padx=10, pady=10)

    def register_car(self):
        # 차량 등록 버튼 클릭 시 실행되는 함수
        owner = self.owner_entry.get()
        carnum = self.carnum_entry.get()
        model = self.model_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        try:
            cursor = self.connection.cursor()
            
            # 차량 등록 SQL 쿼리 실행
            sql_query = f"INSERT INTO ENROLLEDCAR (NAME, CARNUM, MODEL, PHONE, ADDRESS) VALUES ('{owner}', '{carnum}', '{model}', '{phone}', '{address}')"
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
            sql_query = f"SELECT NAME, PHONE, ADDRESS FROM ENROLLEDCAR WHERE CARNUM LIKE '%{carnum}%'"
            cursor.execute(sql_query)
            
            # 결과 가져오기
            row = cursor.fetchone()  # 하나의 행만 가져옴
            
            if row:
                # 결과 출력
                owner_name, phone, address = row
                
                # 출력 형식에 맞게 텍스트 박스에 설정
                self.search_result_text.delete(1.0, tk.END)
                self.search_result_text.insert(tk.END, f"소유자: {owner_name}\n")
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
