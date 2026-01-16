from sqlalchemy.ext.asyncio import Asyncsession
from sqlalchemy import select
from sqlalchemy.orm import joinedload


from infrastructure.databases.postgresql.models.cart import Cart
from infrastructure.databases.postgresql.models.product import Product
from infrastructure.repositories.postgresql.product.exceptions import ProductNotFound
from infrastructure.repositories.postgresql.cart.exceptions import CartNotFound
from src.api.v1.cart.models import CartBase, CartCreate, CartUpdate, CartItem
from src.api.v1.security import get_current_user


class PostgreSQLCartRepository:
    def __init__(self, session: Asyncsession):
        self._session = session
    
    async def get_cart(self, token, cart_id: int) -> CartBase:
        user_id = get_current_user(token)
        query = select(Cart).where(Cart.id == cart_id, Cart.user_id == user_id)
        result = await self._session.execute(query)
        cart = result.scalar_one_or_none()

        if cart is None:
            raise CartNotFound()

        return cart
    
    async def list_carts(self, token, limit: int, offset: int) -> list[CartBase]:
        user_id = get_current_user(token)
        query = select(Cart).where(Cart.user_id == user_id).limit(limit).offset(offset)
        result = await self._session.execute(query)
        carts = result.scalars().all()
        return carts
    
    async def create_cart(self, token, payload: CartCreate) -> CartBase:
        user_id = get_current_user(token)
        cart = payload.model_dump()

        cart_items_data = cart.pop('cart_items', [])
        cart_items = []
        total_amount = 0
        for item_data in cart_items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']

            query = select(Product).where(Product.id == product_id)
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()

            if product is None:
                raise ProductNotFound()

            subtotal = quantity * product.price * (product.discount_percentage / 100)
            cart_item = CartItem(product_id=product_id, quantity=quantity, subtotal=subtotal)
            total_amount += subtotal

            cart_items.append(cart_item)
        
        self._session.add(Cart(user_id=user_id, total_amount=total_amount, cart_items=cart_items, **cart))
        await self._session.flush()

        schema = CartCreate(
            cart_items=cart_items
        )
        return schema

    async def update_cart(self, token, cart_id: int, payload: CartUpdate) -> None:
        user_id = get_current_user(token)
        query = select(Cart).where(Cart.id == cart_id, Cart.user_id == user_id)
        result = await self._session.execute(query)
        cart = result.scalar_one_or_none()

        if cart is None:
            raise CartNotFound()

        query = select(CartItem).where(CartItem.cart_id == cart_id)
        result = await self._session.execute(query)
        cart_items = result.scalars().all()
        self._session.delete(cart_items)

        for item in cart_items:
            self._session.delete(item)

        for item in payload.cart_items:
            product_id = item.product_id
            quantity = item.quantity

            query = select(Product).where(Product.id == product_id)
            result = await self._session.execute(query)
            product = result.scalar_one_or_none()

            if product is None:
                raise ProductNotFound()

            subtotal = quantity * product.price * (product.discount_percentage / 100)
            cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity, subtotal=subtotal)

            self._session.add(cart_item)
        
        cart.total_amount = sum(item.subtotal for item in cart.cart_items)
        await self._session.flush()
        return
    
    async def delete_cart(self, token, cart_id: int) -> None:
        user_id = get_current_user(token)
        query = (select(Cart)
        .options(joinedload(Cart.cart_items)
        .joinedload(CartItem.product))
        .where(Cart.id == cart_id, Cart.user_id == user_id))
        result = await self._session.execute(query)
        cart = result.scalar_one_or_none()

        if cart is None:
            raise CartNotFound()

        self._session.delete(cart)
        await self._session.flush()
        return
    