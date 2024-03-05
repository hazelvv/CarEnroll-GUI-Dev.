import tkinter as tk
from tkinter import messagebox
import cx_Oracle
import cv2
import numpy as np

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
        
        # 차량번호 레이블과 엔트리
        self.search_label = tk.Label(master, text="차량번호:")
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.search_entry = tk.Entry(master)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 검색 버튼
        self.search_button = tk.Button(master, text="검색", command=self.search_by_carnum)
        self.search_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)
        
        # # 검색 결과 텍스트 박스
        # self.result_text = tk.Text(master, height=20, width=100)
        # self.result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        # 소유자 레이블과 텍스트 박스
        self.owner_label = tk.Label(master, text="소 유 자:")
        self.owner_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.owner_text = tk.Text(master, height=5, width=30)
        self.owner_text.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)
        
        # 전화번호 레이블과 텍스트 박스
        self.phone_label = tk.Label(master, text="전화번호:")
        self.phone_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.phone_text = tk.Text(master, height=5, width=30)
        self.phone_text.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)
        
        # 주소 레이블과 텍스트 박스
        self.address_label = tk.Label(master, text="주  소:")
        self.address_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.address_text = tk.Text(master, height=5, width=30)
        self.address_text.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # 차량 이미지 가져오기 테스트
        # self.result_text = tk.Text(master, height=20, width=100)
        # self.result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
    def display_result(self, results, columns):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"{' | '.join(columns)}\n")
        self.result_text.insert(tk.END, "-" * (len(columns) * 20) + "\n")
        for row in results:
            self.result_text.insert(tk.END, f"{row}\n")
    
    def search_by_carnum(self):
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
                
                # 출력 형식에 맞게 텍스트 위젯에 설정
                self.owner_text.delete(1.0, tk.END)
                self.owner_text.insert(tk.END, f"{owner_name}")
                
                self.phone_text.delete(1.0, tk.END)
                self.phone_text.insert(tk.END, f"{phone}")
                
                self.address_text.delete(1.0, tk.END)
                self.address_text.insert(tk.END, f"{address}")
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
