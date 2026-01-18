class CartNotFound(Exception):
    def __init__(self):
        super().__init__('Cart not found.')