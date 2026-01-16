class CategoryNotFound(Exception):
    def __init__(self):
        super().__init__('Category not found.')