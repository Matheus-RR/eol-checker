# eol-checker

Dead simple Python script that checks if anything in your tech stack is approaching end-of-life. Pulls data from [endoflife.date](https://endoflife.date).

Wrote this after getting burned by running Python 3.8 in production 6 months past EOL.

## Usage

```bash
python3 eol_checker.py python nodejs kubernetes postgresql
```

Output:
```
python      3.13.1    Active    EOL: 2029-10    ✅ 3.5 years left
python      3.12.8    Active    EOL: 2028-10    ✅ 2.5 years left
python      3.9.21    EOL       EOL: 2025-10    ❌ EXPIRED
nodejs      22.12.0   Active    EOL: 2027-04    ✅ 1.3 years left
kubernetes  1.32.0    Active    EOL: 2026-02    ⚠️  2 months left
```

No dependencies beyond stdlib. Just pass product names as they appear on endoflife.date.

## License

MIT
