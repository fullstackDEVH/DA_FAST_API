from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import User, Apartment, Contract
from datetime import datetime, timedelta


class Statistical:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def statistical_admin(self):
        total_user = self.db.query(func.count(User.id)).scalar()
        total_contract = self.db.query(func.count(Contract.id)).scalar()
        total_apartment = self.db.query(func.count(Apartment.id)).scalar()

        current_week_start = datetime.utcnow() - timedelta(
            days=datetime.utcnow().weekday()
        )
        total_user_current_week = (
            self.db.query(func.count(User.id))
            .filter(User.created_at >= current_week_start)
            .scalar()
        )
        total_contract_current_week = (
            self.db.query(func.count(Contract.id))
            .filter(Contract.start_date >= current_week_start)
            .scalar()
        )
        total_apartment_current_week = (
            self.db.query(func.count(Apartment.id))
            .filter(Apartment.created_at >= current_week_start)
            .scalar()
        )

        # Lấy tổng số lượng người dùng, hợp đồng và căn hộ cho tuần trước
        previous_week_start = current_week_start - timedelta(days=7)
        total_user_previous_week = (
            self.db.query(func.count(User.id))
            .filter(
                User.created_at >= previous_week_start,
                User.created_at < current_week_start,
            )
            .scalar()
        )
        total_contract_previous_week = (
            self.db.query(func.count(Contract.id))
            .filter(
                Contract.start_date >= previous_week_start,
                Contract.start_date < current_week_start,
            )
            .scalar()
        )
        total_apartment_previous_week = (
            self.db.query(func.count(Apartment.id))
            .filter(
                Apartment.created_at >= previous_week_start,
                Apartment.created_at < current_week_start,
            )
            .scalar()
        )

        # Tính toán phần trăm thay đổi
        user_change_percentage = (
            (
                (total_user_current_week - total_user_previous_week)
                / total_user_previous_week
            )
            * 100
            if total_user_previous_week != 0
            else 0
        )
        contract_change_percentage = (
            (
                (total_contract_current_week - total_contract_previous_week)
                / total_contract_previous_week
            )
            * 100
            if total_contract_previous_week != 0
            else 0
        )
        apartment_change_percentage = (
            (
                (total_apartment_current_week - total_apartment_previous_week)
                / total_apartment_previous_week
            )
            * 100
            if total_apartment_previous_week != 0
            else 0
        )

        # Tạo danh sách kết quả
        result_list = [
            {
                "title": "Total Users",
                "value": total_user,
                "change": round(
                    user_change_percentage, 2
                ),  # Làm tròn đến 2 chữ số thập phân
            },
            {
                "title": "Total Contracts",
                "value": total_apartment,
                "change": round(contract_change_percentage, 2),
            },
            {
                "title": "Total Apartments",
                "value": total_contract,
                "change": round(apartment_change_percentage, 2),
            },
        ]

        # In danh sách kết quả
        return result_list

    async def get_chart_admin(self):
        current_date = datetime.utcnow()

        # Tính toán ngày bắt đầu và kết thúc của 7 ngày gần nhất
        result_list = []

        # Thống kê người dùng và hợp đồng trong 7 ngày gần nhất
        for i in range(7):
            start_of_day = current_date - timedelta(days=i)
            end_of_day = start_of_day + timedelta(days=1)

            user_count = (
                self.db.query(func.count(User.id).label("user_count"))
                .filter(User.created_at.between(start_of_day, end_of_day))
                .scalar()
            )

            contract_count = (
                self.db.query(func.count(Contract.id).label("contract_count"))
                .filter(Contract.created_at.between(start_of_day, end_of_day))
                .scalar()
            )

            # Tạo một từ điển để lưu trữ thông tin ngày và số lượng người dùng, hợp đồng
            result_dict = {
                "name": start_of_day.strftime("%Y-%m-%d"),
                "User_Count": user_count,
                "Contract_Count": contract_count,
            }

            # Thêm từ điển vào danh sách kết quả
            result_list.append(result_dict)

        return result_list
