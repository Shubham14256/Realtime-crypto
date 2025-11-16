# Contributing to Cryptocurrency Data Server

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive of all contributors
- Focus on constructive feedback
- Report any inappropriate behavior to the maintainers

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git version control

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/historical-cryptocurrency.git
   cd historical-cryptocurrency
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-asyncio  # Development dependencies
   ```

4. **Verify setup**
   ```bash
   pytest test_main.py -v
   ```

## Development Workflow

### Branching Strategy

- `main` - Production-ready code
- `develop` - Development branch for integration
- `feature/description` - Feature branches for new functionality
- `bugfix/description` - Bug fix branches
- `docs/description` - Documentation updates

### Creating a Pull Request

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Add comments for complex logic
   - Follow PEP 8 style guidelines

3. **Write or update tests**
   - Add test cases for new features
   - Ensure all tests pass: `pytest test_main.py -v`
   - Aim for >90% code coverage

4. **Update documentation**
   - Update README.md if adding new endpoints
   - Update examples.py with usage examples
   - Update mcp-manifest.json for LLM discovery

5. **Commit your changes**
   ```bash
   git commit -m "feat: Add new feature description"
   ```
   Use conventional commits:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation
   - `test:` - Test additions
   - `refactor:` - Code refactoring
   - `perf:` - Performance improvements

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

## Code Style Guidelines

### Python Style (PEP 8)

```python
# Good: Clear variable names and type hints
async def get_price(symbol: str) -> Dict[str, float]:
    """Fetch current price for cryptocurrency symbol."""
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    return await exchange.fetch_ticker(symbol)

# Bad: Unclear names and no type hints
async def gp(s):
    if s:
        return ex.ft(s)
```

### Naming Conventions

- **Functions**: `snake_case` (e.g., `fetch_price`, `calculate_average`)
- **Classes**: `PascalCase` (e.g., `RateLimiter`, `PerformanceMonitor`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_CACHE_SIZE`, `DEFAULT_TTL`)
- **Private methods**: `_leading_underscore` (e.g., `_validate_symbol`)

### Type Hints

Use type hints for all function signatures:

```python
from typing import Dict, List, Optional, Union

def process_data(
    symbols: List[str],
    config: Optional[Dict[str, Any]] = None
) -> Union[Dict, List]:
    """Process cryptocurrency data."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def fetch_market_data(symbol: str, limit: int = 100) -> Dict:
    """Fetch market data for a cryptocurrency.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTC/USDT')
        limit: Maximum number of records to return
        
    Returns:
        Dictionary containing market data with keys: open, high, low, close, volume
        
    Raises:
        ValueError: If symbol format is invalid
        ConnectionError: If exchange connection fails
        
    Examples:
        >>> data = fetch_market_data('BTC/USDT', limit=50)
        >>> data['close']
        [45000.0, 45100.0, ...]
    """
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest test_main.py -v

# Run specific test class
pytest test_main.py::TestPriceEndpoint -v

# Run with coverage
pytest test_main.py --cov=main --cov-report=html
```

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestNewFeature:
    """Test suite for new feature."""
    
    def test_valid_input(self):
        """Test with valid input."""
        response = client.get("/endpoint/valid_param")
        assert response.status_code == 200
        assert "expected_key" in response.json()
    
    def test_invalid_input(self):
        """Test with invalid input."""
        response = client.get("/endpoint/invalid_param")
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_async_operation(self):
        """Test async functionality."""
        result = await some_async_function()
        assert result is not None
```

## Performance Considerations

### Best Practices

1. **Use caching**
   - Cache frequently requested data with TTL
   - Monitor cache hit rates in `/analytics` endpoint

2. **Optimize database queries**
   - Use connection pooling
   - Minimize round-trips to exchange API

3. **Implement rate limiting**
   - Respect exchange rate limits
   - Use token bucket algorithm for client rate limiting

4. **Monitor performance**
   - Check `/metrics` endpoint for response times
   - Monitor health score with `/health-score` endpoint
   - Review cache analytics at `/analytics`

### Benchmarking

Run performance tests before and after changes:

```bash
# Create benchmark script
python -c "
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
start = time.time()
for _ in range(100):
    client.get('/price/BTC/USDT')
print(f'100 requests: {time.time() - start:.2f}s')
"
```

## Documentation

### README Updates

When adding new features:

1. Add section to README.md
2. Include API endpoint documentation
3. Add usage examples
4. Update table of contents

### API Documentation

Document all endpoints in mcp-manifest.json:

```json
{
  "endpoint": "/your-endpoint",
  "method": "GET",
  "parameters": [...],
  "description": "Clear description",
  "example": {...}
}
```

## Reporting Issues

### Bug Reports

Include:
- Python version and OS
- Installed package versions (`pip freeze`)
- Minimal code to reproduce
- Expected vs actual behavior
- Error messages and stack traces

### Feature Requests

Describe:
- Use case for the feature
- How it benefits users
- Possible implementation approach
- Alternatives considered

## Review Process

1. Maintainers will review your PR within 3-5 business days
2. Address any requested changes
3. Ensure CI/CD checks pass
4. Squash commits if requested
5. Merge upon approval

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open an issue for bugs and features
- Check existing issues before creating new ones
- Ask questions in issue discussions
- Email maintainers for private concerns

---

Thank you for contributing! Your efforts help make this project better for everyone. 🙌
