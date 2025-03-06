# Income categories
INCOME_CATEGORIES = [
    'Зарплата', 'Калими', 'Подарунок', 'Інше'
]

# Expense categories
EXPENSE_CATEGORIES = [
    'Їжа', 'Хазяйство', 'Підписки', 'Здоровя', 'Комунальні послуги',
    'Транспорт', 'Одяг', 'Краса', 'Подорожі', 'Розваги', 'Освіта',
    'Покупки', 'Заощадження', 'Інші витрати'
]

# SQL statements for creating tables
CREATE_CATEGORIES_TABLE = '''
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type ENUM('income', 'expense') NOT NULL
)
'''

CREATE_TRANSACTIONS_TABLE = '''
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    date DATETIME NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
'''
