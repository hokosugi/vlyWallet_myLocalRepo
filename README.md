# Vly.money Wallet Leaderboard

A leaderboard application for tracking Vly.money wallet users' transaction metrics with a sophisticated point calculation system. The platform provides user registration, secure admin authentication, leaderboard displays, and detailed transaction history views.

## Features

- **User Registration**: Simple registration system for Vly.money wallet users
- **Admin Authentication**: Environment-based secure admin authentication system
- **Leaderboard System**: 
  - Transaction-based points
  - Frequency bonuses
  - Weekly streak rewards
- **Transaction Tracking**:
  - Detailed transaction history
  - Statistical breakdowns
  - Points calculation system
- **Data Visualization**:
  - Interactive charts using Chart.js
  - Leaderboard rankings
  - Point distributions
  - Transaction analytics
- **Automated Updates**:
  - Scheduled weekly transaction updates
  - Git repository synchronization
  - Selective commit pushing
- **Internationalization**:
  - English and Japanese language support
  - Localized interface elements

## Technology Stack

- **Backend**: Python 3.11+ with Flask
- **Database**: PostgreSQL
- **Frontend**: 
  - HTML/CSS with Bootstrap
  - Chart.js for data visualization
- **Authentication**: Flask-Login
- **Testing**: 
  - pytest for unit testing
  - Coverage reporting
- **Code Quality**:
  - flake8 for linting
  - bandit for security scanning
- **CI/CD**: GitHub Actions
- **Deployment**: Replit

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hokosugi/VlyWalletLeadersboard.git
cd VlyWalletLeadersboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Required environment variables
DATABASE_URL=postgresql://user:password@host:port/dbname
ADMIN_PASSWORD=your_admin_password
GITHUB_TOKEN=your_github_token
FLASK_SECRET_KEY=your_secret_key
```

4. Initialize the database:
```bash
python app.py
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

3. Register as a user or log in as admin:
   - Regular users can register with their Vly.money wallet ID
   - Admin login available at `/admin/login`

## API Documentation

### User Registration
- **Endpoint**: `/register`
- **Method**: POST
- **Parameters**: `user_id`

### Transaction History
- **Endpoint**: `/transaction-history/<user_id>`
- **Method**: GET
- **Response**: User's transaction history and points

### Leaderboard
- **Endpoint**: `/leaderboard`
- **Method**: GET
- **Response**: Top users by points, transaction count, and amount

### Data Export
- **Endpoint**: `/export-csv`
- **Method**: GET
- **Response**: CSV file with transaction data
- **Authentication**: Admin only

## Points System

Points are calculated based on:
1. Transaction Count: 10 points per transaction
2. Transaction Amount: 1 point per $100
3. Large Transaction Bonus: 50 points per $1000
4. Frequency Bonus: 5 points per daily transaction
5. Weekly Streak: 25 points per consecutive week

## Testing

Run the test suite:
```bash
pytest
```

Generate coverage report:
```bash
pytest --cov=. --cov-report=html
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Branch Protection Rules
- Required pull request reviews
- Linear history required
- No force pushes
- No deletions

## Security

- Environment-based configuration
- Secure password hashing
- CSRF protection
- SQL injection prevention
- Regular security scanning with bandit

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Vly.money for the wallet integration
- Chart.js for data visualization
- Bootstrap for the UI framework
