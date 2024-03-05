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
        style.configure("CustomTab.TNotebook.Tab", foreground="black", font=("Helvetica", 40))

        # Create a tab control
        self.notebook = ttk.Notebook(master)

        self.notebook.pack(expand=True, fill=tk.BOTH)
       
        # 차량 조회 페이지
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="차량 조회")
        self.setup_search_page(self.search_frame)
        
         # 차량 수정 페이지
        self.modify_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.modify_frame, text="차량 수정")
        self.setup_modify_page(self.modify_frame)

        # 차량 등록 페이지
        self.register_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.register_frame, text="차량 등록")
        self.setup_register_page(self.register_frame)

       

    def setup_search_page(self, frame):
        # 차량 조회 페이지 설정

        # 차량 조회 텍스트
        self.search_label = tk.Label(frame, text="차량번호 입력", width=13, height=5)
        self.search_label.grid(row=0, column=0, padx=5, pady=5)

        # 차량 번호 입력
        self.search_entry = tk.Entry(frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        # 검색 버튼
        self.search_button = tk.Button(frame, text="차량검색", command=self.search_by_carnum)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

       
        # 소유자 정보 네모칸
        self.owner_frame = tk.Frame(frame, bg="white")
        self.owner_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

        self.owner_label = tk.Label(self.owner_frame, text="소유자:", width=8, height=2, bg="white")
        self.owner_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.owner_value = tk.Label(self.owner_frame, text="", width=30, height=2, bg="white")
        self.owner_value.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # 차량번호 정보 네모칸
        self.carnum_frame = tk.Frame(frame, bg="white")
        self.carnum_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

        self.carnum_label = tk.Label(self.carnum_frame, text="차량번호:", width=8, height=2, bg="white")
        self.carnum_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.carnum_value = tk.Label(self.carnum_frame, text="", width=30, height=2, bg="white")
        self.carnum_value.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # 모델명 정보 네모칸
        self.model_frame = tk.Frame(frame, bg="white")
        self.model_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

        self.model_label = tk.Label(self.model_frame, text="모델명:", width=8, height=2, bg="white")
        self.model_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.model_value = tk.Label(self.model_frame, text="", width=30, height=2, bg="white")
        self.model_value.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # 전화번호 정보 네모칸
        self.phone_frame = tk.Frame(frame, bg="white")
        self.phone_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

        self.phone_label = tk.Label(self.phone_frame, text="전화번호:", width=8, height=2, bg="white")
        self.phone_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.phone_value = tk.Label(self.phone_frame, text="", width=30, height=2, bg="white")
        self.phone_value.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # 주소 정보 네모칸
        self.address_frame = tk.Frame(frame, bg="white")
        self.address_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

        self.address_label = tk.Label(self.address_frame, text="주소:", width=8, height=2, bg="white" )
        self.address_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.address_value = tk.Label(self.address_frame, text="", width=30, height=2, bg="white")
        self.address_value.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)


    def setup_modify_page(self, frame):
        # 차량 수정 페이지 설정

        # 차량 번호 입력 레이블 및 엔트리
        self.modify_carnum_label = tk.Label(frame, text="차량번호 입력:", width=13, height=5)
        self.modify_carnum_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.modify_carnum_entry = tk.Entry(frame)
        self.modify_carnum_entry.grid(row=0, column=1, padx=5, pady=5)

        # 검색 버튼
        self.modify_search_button = tk.Button(frame, text="차량검색", command=self.search_car_for_modify)
        self.modify_search_button.grid(row=0, column=2, padx=10, pady=10)

        # 수정할 정보 입력 레이블 및 엔트리
        #소유자
        self.modify_owner_frame = tk.Frame(frame, bg="white")
        self.modify_owner_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

        self.modify_owner_label = tk.Label(self.modify_owner_frame, text="소유자:", width=8, height=2, bg="white")
        self.modify_owner_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.modify_owner_value = tk.Label(self.modify_owner_frame, text="", width=30, height=2, bg="white")
        self.modify_owner_value.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.modify_owner_entry = tk.Entry(self.modify_owner_frame)
        self.modify_owner_entry.grid(row=1, column=1, padx=5, pady=5)


        # 모델명
        self.modify_model_frame = tk.Frame(frame, bg="white")
        self.modify_model_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)
        
        self.modify_model_label = tk.Label(self.modify_model_frame, text="모델명:", width=8, height=2, bg="white")
        self.modify_model_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.modify_model_value = tk.Label(self.modify_model_frame, text="", width=30, height=2, bg="white")
        self.modify_model_value.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.modify_model_entry = tk.Entry(self.modify_model_frame)
        self.modify_model_entry.grid(row=2, column=1, padx=5, pady=5)



        #전화번호
        self.modify_phone_frame = tk.Frame(frame, bg="white")
        self.modify_phone_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)
        
        self.modify_phone_label = tk.Label(self.modify_phone_frame, text="전화번호:", width=8, height=2, bg="white")
        self.modify_phone_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.modify_phone_value = tk.Label(self.modify_phone_frame, text="", width=30, height=2, bg="white")
        self.modify_phone_value.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.modify_phone_entry = tk.Entry(self.modify_phone_frame)
        self.modify_phone_entry.grid(row=3, column=1, padx=5, pady=5)

         #주소
        self.modify_address_frame = tk.Frame(frame, bg="white")
        self.modify_address_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

        self.modify_address_label = tk.Label(self.modify_address_frame, text="주소:", width=8, height=2, bg="white")
        self.modify_address_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.modify_phone_value = tk.Label(self.modify_address_frame, text="", width=30, height=2, bg="white")
        self.modify_phone_value.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.modify_address_entry = tk.Entry(self.modify_address_frame)
        self.modify_address_entry.grid(row=4, column=1, padx=5, pady=5)
        

        # 수정 버튼
        self.modify_button = tk.Button(frame, text="수정", command=self.modify_car,  width=8)
        self.modify_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


    def modify_car(self):
        # 1. 수정할 차량의 번호를 입력란에서 가져옵니다.
        carnum = self.modify_carnum_entry.get()

        # 2. 수정할 소유자, 모델명, 전화번호, 주소를 각각 입력란에서 가져옵니다.
        owner = self.modify_owner_entry.get()
        model = self.modify_model_entry.get()
        phone = self.modify_phone_entry.get()
        address = self.modify_address_entry.get()

        try:
            cursor = self.connection.cursor()
            
            # 3. 데이터베이스에 해당 차량 번호를 가진 레코드를 업데이트하는 SQL 쿼리를 실행합니다.
            sql_query = """
                        UPDATE ENROLLEDCAR 
                        SET 소유자 = :owner, 모델명 = :model, 전화번호 = :phone, 주소 = :address
                        WHERE 차량번호 = :carnum
                        """

            cursor.execute(sql_query, owner=owner, model=model, phone=phone, address=address, carnum=carnum)
            
            self.connection.commit()  # 변경 사항을 커밋

            # 수정 완료 메시지 표시
            messagebox.showinfo("수정 완료", "차량 정보가 성공적으로 수정되었습니다.")
            
            # 커서 닫기
            cursor.close()
        except cx_Oracle.Error as error:
            messagebox.showerror("오류", f"차량 정보 수정 중 오류 발생: {error}")
        
    def search_car_for_modify(self):
        # 수정할 차량의 번호를 입력란에서 가져옵니다.
        carnum = self.modify_carnum_entry.get()

        try:
            cursor = self.connection.cursor()
            
            # 차량번호로 소유자 정보 검색
            sql_query = f"SELECT 소유자, 모델명, 전화번호, 주소 FROM ENROLLEDCAR WHERE 차량번호 LIKE '%{carnum}%'"
            cursor.execute(sql_query)
            
            # 결과 가져오기
            row = cursor.fetchone()  # 하나의 행만 가져옴
            
            if row:
                # 결과 출력
                owner, model, phone, address = row
                
                # 검색된 정보를 각각의 입력란에 표시
                self.modify_owner_entry.delete(0, tk.END)
                self.modify_owner_entry.insert(0, owner)

                self.modify_model_entry.delete(0, tk.END)
                self.modify_model_entry.insert(0, model)

                self.modify_phone_entry.delete(0, tk.END)
                self.modify_phone_entry.insert(0, phone)

                self.modify_address_entry.delete(0, tk.END)
                self.modify_address_entry.insert(0, address)
            else:
                # 검색된 결과가 없는 경우 메시지 출력
                messagebox.showinfo("검색 결과", "해당하는 차량번호의 정보가 없습니다.")
            
            # 커서 닫기
            cursor.close()
        except cx_Oracle.Error as error:
            messagebox.showerror("오류", f"Oracle 데이터베이스 연결 중 오류 발생: {error}")


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

    # def register_car(self):
    #     # 차량 등록 함수
    #     fields = ["소유자", "차량번호", "모델명", "전화번호", "주소"]
    #     values = [self.register_entries[field].get() for field in fields]

    #     try:
    #         cursor = self.connection.cursor()
            
    #         # 차량 등록 SQL 쿼리 실행
    #         sql_query = f"INSERT INTO ENROLLEDCAR ({', '.join(fields)}) VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}')"

    #         cursor.execute(sql_query)
    #         self.connection.commit()  # 변경 사항을 커밋

    #         # 등록 완료 메시지 표시
    #         messagebox.showinfo("등록 완료", "차량이 성공적으로 등록되었습니다.")
            
    #         # 커서 닫기
    #         cursor.close()
    #     except cx_Oracle.Error as error:
    #         messagebox.showerror("오류", f"차량 등록 중 오류 발생: {error}")

    
    def register_car(self):
        # 차량 등록 함수
        fields = ["소유자", "차량번호", "모델명", "전화번호", "주소"]
        values = [self.register_entries[field].get() for field in fields]

        try:
            cursor = self.connection.cursor()
            
            # 차량 등록 SQL 쿼리 실행 (바인딩 사용)
            sql_query = """
                        INSERT INTO ENROLLEDCAR 
                        (소유자, 차량번호, 모델명, 전화번호, 주소) 
                        VALUES 
                        (:owner, :carnum, :model, :phone, :address)
                        """

            # 바인딩을 사용하여 SQL 쿼리 실행
            cursor.execute(sql_query, owner=values[0], carnum=values[1], model=values[2], phone=values[3], address=values[4])
            
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
                
                # 조회된 정보를 네모칸에 표시
                self.owner_value.config(text=owner_name)
                self.carnum_value.config(text=carnum)
                self.model_value.config(text=model)
                self.phone_value.config(text=phone)
                self.address_value.config(text=address)
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
