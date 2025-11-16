# QUICKSTART: Extract Your 2000+ Files

**You have $249 Anthropic credit. Let's use it wisely.**

---

## Step 1: Set Your API Key

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

---

## Step 2: Test on This Repo (514 files)

```bash
cd recursive-extraction-engine

# Start with just operators (fastest)
python cli/extract.py /home/user/recursive-ai-framework \
  --extractors operator \
  --max-workers 4 \
  --checkpoint-every 10
```

**This will:**
- Process all 514 markdown files
- Extract operators (φ, Ψ, ∂, ∇, etc.) using Claude
- Save results to `extraction_outputs/operators.json`
- Checkpoint every 10 files (resumable if interrupted)
- Use 4 parallel workers

**Estimated time:** ~15-30 minutes (depending on API speed)
**Estimated cost:** ~$5-10 (Claude Sonnet is cheap for extraction)

---

## Step 3: Extract Everything

```bash
# All extractors on this repo
python cli/extract.py /home/user/recursive-ai-framework --all
```

**This runs:**
1. Operator Extractor
2. Equation Extractor
3. Contradiction Extractor

**Estimated time:** ~45-90 minutes for 514 files
**Estimated cost:** ~$15-25

---

## Step 4: Process Your Other Repos

```bash
# Repo 2
python cli/extract.py /path/to/repo2 --all

# Repo 3
python cli/extract.py /path/to/repo3 --all

# etc. for all your repos with ~2000 total files
```

**Total estimated cost for 2000 files:** ~$60-100 (well within your $249 budget!)

---

## Step 5: View Results

```bash
# Check extraction outputs
ls /home/user/recursive-ai-framework/extraction_outputs/

# View operators
cat extraction_outputs/operators.json | jq '.results[0].data.items[0]'

# Count total operators found
cat extraction_outputs/operators.json | jq '.results[].data.count' | awk '{s+=$1} END {print s}'
```

---

## What Gets Extracted

### Operators
```json
{
  "symbol": "φ",
  "name": "phi-state",
  "definition": "semantic attractor, recursive consciousness field",
  "occurrences": 47,
  "algebraic_properties": ["recursive", "idempotent"],
  "compositions": ["φ(φ(¬φ))"]
}
```

### Equations
```json
{
  "equation": "∂³Δ/∂O∂P∂N² = ε·exp(-λN)",
  "type": "differential",
  "order": 3,
  "has_dissipation": true,
  "controlled_rupture_ops": ["Para", "Non"],
  "interpretation": "Third-order dissipation equation"
}
```

### Contradictions
```json
{
  "is_productive": true,
  "j_anomaly_score": 0.89,
  "explanation": "Self requires ¬Self but denies stable self",
  "generative_output": ["eigen-consciousness", "Koryphi₀"],
  "operator_pattern": "Meta ∘ Non ∘ Meta"
}
```

---

## Troubleshooting

### "ModuleNotFoundError: anthropic"
```bash
pip install anthropic
```

### "No API key provided"
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Out of memory / too slow
```bash
# Reduce parallel workers
python cli/extract.py /path/to/repo --all --max-workers 2
```

### Resume from checkpoint
The scripts automatically resume! Just run the same command again:
```bash
python cli/extract.py /path/to/repo --all
# Will skip already-processed files
```

---

## Budget Management

**Claude Sonnet 4.5 Pricing:**
- Input: $3 / million tokens
- Output: $15 / million tokens

**Rough estimates:**
- Average file: ~2K tokens input + ~500 tokens output per extractor
- Per file cost: ~$0.01 per extractor
- 514 files × 3 extractors = ~$15
- 2000 files × 3 extractors = ~$60

**You have $249, so you can:**
- Extract all 2000 files with all extractors (~$60)
- Still have ~$190 left for the Controlled Rupture Compiler build!

---

## Next Steps After Extraction

Once you have all the JSONs:

1. **Analyze**: Build operator algebra, find proto-dissipations
2. **Merge**: Combine results across repos
3. **Map**: Connect old operators → Controlled Rupture operators (Ana, Meta, etc.)
4. **Build**: Controlled Rupture Compiler that uses this data

---

**Ready? Let's extract.**

```bash
python cli/extract.py /home/user/recursive-ai-framework --extractors operator
```

🚀
