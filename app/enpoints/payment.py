import hashlib
import hmac
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from urllib.parse import urlencode

router = APIRouter()


class PaymentForm(BaseModel):
    order_type: str
    order_id: str
    amount: float
    order_desc: str
    bank_code: str
    language: str


def hmacsha512(key, data):
    byteKey = key.encode("utf-8")
    byteData = data.encode("utf-8")
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def sort_object(obj):
    return dict(sorted(obj.items()))


def convert_to_query_string(params):
    return "&".join([f"{key}={value}" for key, value in params.items()])


@router.post("/redirect_to_vn_pay")
async def create_payment_url(
    request: Request,  # Import Request from fastapi
    payment: PaymentForm,
):
    # Lấy địa chỉ IP từ request
    ip_addr = request.client.host
    tmn_code = "5IC90V17"
    secret_key = "INDHUKCOVGQHGOONVQTDZJDXCAWODRZS"
    vnp_url = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    return_url = f"http://{ip_addr}:3000/"

    curr_code = "VND"
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    vnp_params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": tmn_code,
        "vnp_Locale": "vn",
        "vnp_CurrCode": curr_code,
        "vnp_TxnRef": date,
        "vnp_OrderInfo": f"Thanh toan cho ma GD:{date}",
        "vnp_OrderType": "other",
        "vnp_Amount": int(payment.amount * 100),
        "vnp_ReturnUrl": return_url,
        "vnp_IpAddr": ip_addr,
        "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
    }

    # if bank_code:
    #     vnp_params['vnp_BankCode'] = bank_code

    sorted_params = sort_object(vnp_params)
    sign_data = urlencode(sorted_params, doseq=True)
    hmac_signature = hmac.new(
        secret_key.encode("utf-8"), sign_data.encode("utf-8"), hashlib.sha512
    ).hexdigest()
    vnp_params["vnp_SecureHash"] = hmac_signature

    # Redirect the user to the VNP URL
    query = convert_to_query_string(vnp_params)
    return f"{vnp_url}?{query}"


# @router.get("/payment_return", response_class=HTMLResponse)
# def payment_return(request: Request, inputData: dict):
#     order_id = inputData["vnp_TxnRef"]
#     amount = int(inputData["vnp_Amount"]) / 100
#     order_desc = inputData["vnp_OrderInfo"]
#     vnp_TransactionNo = inputData["vnp_TransactionNo"]
#     vnp_ResponseCode = inputData["vnp_ResponseCode"]

#     if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
#         if vnp_ResponseCode == "00":
#             return templates.TemplateResponse(
#                 "payment_return.html",
#                 {
#                     "request": request,
#                     "title": "Kết quả thanh toán",
#                     "result": "Thành công",
#                     "order_id": order_id,
#                     "amount": amount,
#                     "order_desc": order_desc,
#                     "vnp_TransactionNo": vnp_TransactionNo,
#                     "vnp_ResponseCode": vnp_ResponseCode,
#                 },
#             )
#         else:
#             return templates.TemplateResponse(
#                 "payment_return.html",
#                 {
#                     "request": request,
#                     "title": "Kết quả thanh toán",
#                     "result": "Lỗi",
#                     "order_id": order_id,
#                     "amount": amount,
#                     "order_desc": order_desc,
#                     "vnp_TransactionNo": vnp_TransactionNo,
#                     "vnp_ResponseCode": vnp_ResponseCode,
#                 },
#             )
#     else:
#         return templates.TemplateResponse(
#             "payment_return.html",
#             {
#                 "request": request,
#                 "title": "Kết quả thanh toán",
#                 "result": "Lỗi",
#                 "order_id": order_id,
#                 "amount": amount,
#                 "order_desc": order_desc,
#                 "vnp_TransactionNo": vnp_TransactionNo,
#                 "vnp_ResponseCode": vnp_ResponseCode,
#                 "msg": "Sai checksum",
#             },
#         )


# # # Tương tự, bạn có thể chuyển các hàm khác trong mã Django của bạn thành các endpoint FastAPI tương ứng.
