# Contributing to H2O Satellite Water Shield System

First off, thank you for considering contributing to H2O! 🛰️💧

The following is a set of guidelines for contributing to this project. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to fostering an open and welcoming environment. Please be respectful and constructive in your interactions.

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, configuration)
- **Describe the behavior you observed** and what you expected
- **Include Python version** and operating system details

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any similar projects** that have this feature

### 🔬 Areas for Contribution

We welcome contributions in these areas:

#### Scientific Enhancements
- More accurate radiation models (solar particle events, Van Allen belts)
- Advanced thermal models (multi-layer insulation, radiative heat transfer)
- Validation against real satellite data
- Additional orbital mechanics calculations

#### Engineering Features
- Phase change material (PCM) integration beyond water
- Multi-layer shield optimization
- Real-time orbital position tracking
- Integration with satellite frameworks (cubesat, etc.)

#### Web Application
- Interactive 3D visualizations
- Historical data tracking and charts
- Real-time simulation controls
- Mobile-responsive design improvements

#### Documentation
- Tutorial notebooks
- API documentation improvements
- Use case examples (Mars missions, lunar gateway, etc.)
- Translation to other languages

#### Testing
- Additional unit tests
- Integration tests for Flask app
- Performance benchmarks
- Edge case coverage

### 🔧 Pull Request Process

1. **Fork the repository** and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards:
   - Follow PEP 8 style guide for Python code
   - Include docstrings for all functions and classes
   - Add type hints where appropriate
   - Keep functions focused and modular

3. **Add tests** for new functionality:
   ```bash
   python test_water_shield.py
   ```

4. **Update documentation**:
   - Update README.md if you change functionality
   - Add docstrings to new functions/classes
   - Update examples if APIs change

5. **Commit your changes**:
   ```bash
   git commit -m "feat: add solar wind radiation model"
   ```
   
   Use conventional commit messages:
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes
   - `test:` - Test additions/changes
   - `refactor:` - Code refactoring
   - `style:` - Formatting, missing semicolons, etc.
   - `perf:` - Performance improvements

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**:
   - Fill in the PR template
   - Link any related issues
   - Ensure all tests pass
   - Request review from maintainers

### 📝 Coding Standards

#### Python Code Style
```python
def calculate_radiation_dose(
    thickness_cm: float,
    exposure_days: float = 1.0
) -> Dict[str, float]:
    """
    Calculate radiation dose reduction.
    
    Args:
        thickness_cm: Shield thickness in centimeters
        exposure_days: Duration of exposure in days
        
    Returns:
        Dictionary containing dose metrics
        
    Example:
        >>> dose = calculate_radiation_dose(10.0, 7.0)
        >>> print(dose['reduction_percent'])
        77.7
    """
    # Implementation here
    pass
```

#### Documentation Style
- Use Google-style docstrings
- Include examples for complex functions
- Document all parameters and return values
- Explain the physics/math behind calculations

#### Testing Standards
- Write tests for all new functions
- Aim for >80% code coverage
- Test edge cases and boundary conditions
- Use descriptive test names

### 🚀 Development Setup

1. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/H2O.git
   cd H2O
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**:
   ```bash
   python test_water_shield.py
   ```

5. **Run the Flask app**:
   ```bash
   python app.py
   ```

### 📊 Project Structure

```
H2O/
├── water_shield.py          # Core system implementation
├── test_water_shield.py     # Unit tests
├── app.py                   # Flask web application
├── templates/
│   └── index.html          # Web dashboard
├── example.py              # Example usage
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── CONTRIBUTING.md        # This file
└── LICENSE                # MIT License
```

### 🤝 Getting Help

- 💬 Open a [Discussion](https://github.com/stephenvegagarcia/H2O/discussions) for questions
- 🐛 Create an [Issue](https://github.com/stephenvegagarcia/H2O/issues) for bugs
- 📧 Reach out to maintainers for guidance

### 📜 License

By contributing to H2O, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to space technology! 🚀**

Your contributions help advance our understanding and implementation of sustainable space systems.
