"""
Payment Service Abstraction
Razorpay-ready payment integration
"""
import os
from typing import Optional
from datetime import datetime, timezone

class PaymentService:
    """
    Payment service abstraction (Razorpay-ready)
    """
    
    def __init__(self):
        self.key_id = os.environ.get("RAZORPAY_KEY_ID")
        self.key_secret = os.environ.get("RAZORPAY_KEY_SECRET")
        self.enabled = bool(self.key_id and self.key_secret)
    
    async def create_order(
        self,
        amount: float,
        currency: str = "INR",
        receipt: Optional[str] = None,
        notes: Optional[dict] = None
    ) -> dict:
        """
        Create a payment order
        Amount should be in currency units (e.g., 999 for ₹999)
        """
        if not self.enabled:
            return {
                "status": "mocked",
                "order_id": f"mock_order_{datetime.now(timezone.utc).timestamp()}",
                "amount": amount,
                "currency": currency,
                "message": "Razorpay not configured. Add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET to enable."
            }
        
        # TODO: Integrate with Razorpay
        # import razorpay
        # client = razorpay.Client(auth=(self.key_id, self.key_secret))
        # order = client.order.create({
        #     "amount": int(amount * 100),  # Razorpay uses paise
        #     "currency": currency,
        #     "receipt": receipt,
        #     "notes": notes or {}
        # })
        # return order
        
        return {
            "status": "mocked",
            "order_id": f"mock_order_{datetime.now(timezone.utc).timestamp()}",
            "amount": amount,
            "currency": currency
        }
    
    async def verify_payment(
        self,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str
    ) -> dict:
        """Verify payment signature"""
        if not self.enabled:
            return {
                "status": "mocked",
                "verified": True,
                "message": "Payment verification mocked"
            }
        
        # TODO: Integrate with Razorpay verification
        # import razorpay
        # client = razorpay.Client(auth=(self.key_id, self.key_secret))
        # try:
        #     client.utility.verify_payment_signature({
        #         "razorpay_order_id": razorpay_order_id,
        #         "razorpay_payment_id": razorpay_payment_id,
        #         "razorpay_signature": razorpay_signature
        #     })
        #     return {"verified": True}
        # except:
        #     return {"verified": False}
        
        return {"status": "mocked", "verified": True}
    
    async def get_payment_status(self, payment_id: str) -> dict:
        """Get payment status"""
        if not self.enabled:
            return {
                "status": "mocked",
                "payment_status": "captured",
                "message": "Payment status mocked"
            }
        
        # TODO: Fetch from Razorpay
        return {"status": "mocked", "payment_status": "captured"}

# Singleton instance
payment_service = PaymentService()
