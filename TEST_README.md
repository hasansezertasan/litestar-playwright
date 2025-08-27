# Test Documentation

## Test Structure

### Test Categories

#### 1. Configuration Tests (`test_playwright_config*`)

- Test `PlaywrightConfig` initialization with default values
- Test custom configuration values
- Test different browser types (chromium, firefox, webkit)
- Test headless mode configuration

#### 2. Plugin Tests (`test_playwright_plugin*`)

- Test plugin dependency injection
- Test plugin lifespan integration
- Test full plugin integration with app config

#### 3. Provider Tests (`test_playwright_config_provider*`)

- Test browser provider function
- Test custom state key configuration
- Test state retrieval functionality

#### 4. Lifespan Tests (`test_playwright_lifespan*`)

- Test successful lifespan management
- Test browser launch and cleanup
- Test exception handling during lifespan
- Test different browser types in lifespan

## Test Coverage

### Current Coverage: 95%

- **`config.py`**: 100% coverage ✅
- **`plugin.py`**: 100% coverage ✅
- **`conftest.py`**: 100% coverage ✅

### Coverage Details

#### Fully Covered Components

- `PlaywrightConfig` class initialization and methods
- `PlaywrightPlugin` class and dependency injection
- Lifespan management with proper cleanup
- Browser provider functionality
- Error handling in lifespan context

#### Test Scenarios Covered

- ✅ Default configuration values
- ✅ Custom configuration values
- ✅ All browser types (chromium, firefox, webkit)
- ✅ Headless mode configuration
- ✅ Dependency injection
- ✅ Plugin integration
- ✅ Lifespan management
- ✅ Exception handling
- ✅ State management
- ✅ Browser provider with custom keys

## Running Tests

### Basic Test Execution

```sh
# Run all tests
uv run pytest tests/

# Run with verbose output
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_playwright.py -v
```

### Coverage Analysis

```sh
# Run tests with coverage
uv run pytest tests/ --cov=src/litestar_playwright --cov-report=term-missing

# Generate HTML coverage report
uv run pytest tests/ --cov=src/litestar_playwright --cov-report=html
```

### Test Categories

```sh
# Run only configuration tests
uv run pytest tests/ -k "config" -v

# Run only plugin tests
uv run pytest tests/ -k "plugin" -v

# Run only lifespan tests
uv run pytest tests/ -k "lifespan" -v
```

## Test Patterns

### Mocking Strategy

- **Playwright API**: Mocked to avoid actual browser launches
- **Async Operations**: Properly mocked with `AsyncMock`
- **State Management**: Mocked app state for testing
- **Dependencies**: Mocked dependency injection

### Async Testing

- All tests use `@pytest.mark.anyio` decorator
- Proper async context management
- Lifespan testing with async context managers

### Fixtures

- `anyio_backend`: Sets async backend to asyncio
- `app_test`: Creates test application with mocked Playwright

## Test Quality Metrics

### Test Count: 12 tests

- 3 configuration tests
- 2 plugin tests
- 2 provider tests
- 5 lifespan tests

### Test Types

- **Unit Tests**: 12 (100%)
- **Integration Tests**: 0 (planned for future)
- **End-to-End Tests**: 0 (planned for future)

## Future Test Improvements

### Planned Enhancements

1. **Integration Tests**: Test with real Litestar app and mocked browser
2. **Error Handling Tests**: More comprehensive error scenario testing
3. **Performance Tests**: Test browser launch/cleanup performance
4. **Concurrency Tests**: Test multiple concurrent browser operations

### Missing Test Scenarios

1. **Browser Launch Failures**: Test when browser fails to launch
2. **Network Errors**: Test network-related failures
3. **Resource Cleanup**: Test memory leak scenarios
4. **Configuration Validation**: Test invalid configuration values

## Best Practices

### Test Naming

- Tests follow descriptive naming: `test_<component>_<scenario>`
- Clear docstrings explaining test purpose
- Consistent naming conventions

### Test Organization

- Related tests grouped together
- Logical test flow from simple to complex
- Clear separation of concerns

### Mocking Guidelines

- Mock external dependencies (Playwright API)
- Use realistic mock data
- Verify mock interactions
- Clean up mocks after tests

### Async Testing

- Always use `@pytest.mark.anyio`
- Proper async context management
- Handle async exceptions correctly
- Test both success and failure paths

## Continuous Integration

### GitHub Actions

Tests are automatically run on:
- Pull requests
- Push to main branch
- Release tags

### Quality Gates

- All tests must pass
- Coverage must be >90%
- No linting errors
- No type checking errors

## Troubleshooting

### Common Issues

1. **Mock Not Called**: Check mock setup and patching
2. **Async Context Errors**: Ensure proper async context management
3. **Coverage Gaps**: Add tests for uncovered code paths
4. **Test Isolation**: Ensure tests don't interfere with each other

### Debug Commands

```sh
# Run single test with debug output
uv run pytest tests/test_playwright.py::test_playwright_config -v -s

# Run with maximum verbosity
uv run pytest tests/ -vvv

# Run with coverage and show missing lines
uv run pytest tests/ --cov=src/litestar_playwright --cov-report=term-missing -v
```
