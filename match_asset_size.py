from thefuzz import process
import pandas as pd

# File path
file_path = r'C:\Users\KARUNA\Desktop\KP\Projects\BANK\Copy of 2025 EPCOR Payments Conference - Fall_Attendee List.xlsx'

# Load sheets
bank_info = pd.read_excel(file_path, sheet_name='Fall Conference 2025')
asset_size = pd.read_excel(file_path, sheet_name='AssetSize')

# Clean column names
bank_info.columns = bank_info.columns.str.strip()
asset_size.columns = asset_size.columns.str.strip()

# Clean bank name
def clean_bank_name(name):
    if pd.isna(name):
        return ''
    name = str(name).upper()
    # Remove common suffixes and fluff
    remove_terms = [
        'BANK', 'TRUST', 'COMPANY', 'NATIONAL ASSOCIATION', 'N.A.', 'N.A', 'NA',
        'SSB', 'F.S.B.', 'F.S.B', 'SAVINGS', 'LOAN', 'INC', 'ASSOCIATION', 'CORPORATION', 'CO.', 'CO', 'LIMITED'
    ]
    for term in remove_terms:
        name = name.replace(term, '')
    name = name.replace('&', 'AND')  # Normalize ampersands
    name = ''.join(e for e in name if e.isalnum() or e.isspace())  # Keep alphanum and spaces
    return ' '.join(name.split()).strip()

# Clean names and state
bank_info['clean_name'] = bank_info['Organization Name'].apply(clean_bank_name)
bank_info['state_clean'] = bank_info['State'].astype(str).str.upper().str.strip()

asset_size['clean_name'] = asset_size['Bank Name'].apply(clean_bank_name)
asset_size['state_clean'] = asset_size['State'].astype(str).str.upper().str.strip()

# Group assets by state
asset_grouped_by_state = asset_size.groupby('state_clean')[['clean_name', 'Total Assets (millions)']].apply(lambda df: list(zip(df['clean_name'], df['Total Assets (millions)']))).to_dict()

# Matching logic
def get_best_match(row):
    state = row['state_clean']
    name = row['clean_name']

    if state not in asset_grouped_by_state:
        return None

    choices = [bank for bank, _ in asset_grouped_by_state[state]]
    result = process.extractOne(name, choices, score_cutoff=90)  # Stricter threshold

    if result is None:
        return None

    match, score = result

    # Find matching asset value
    for bank_name, assets in asset_grouped_by_state[state]:
        if bank_name == match:
            return assets
    return None

# Apply matching
bank_info['Bank Asset Size Raw'] = bank_info.apply(get_best_match, axis=1)

# Indian-style formatting
def format_asset_indian(amount):
    if pd.isna(amount):
        return ''
    amount = int(round(amount))
    s = str(amount)
    if len(s) <= 3:
        return '$' + s + '.0'
    else:
        last3 = s[-3:]
        rest = s[:-3]
        # Group in 2s
        rest_grp = ','.join([rest[max(i-2, 0):i] for i in range(len(rest), 0, -2)][::-1])
        return f"${rest_grp},{last3}.0"

# Format the result
bank_info['Bank Asset Size'] = bank_info['Bank Asset Size Raw'].apply(format_asset_indian)

# Drop helper columns
bank_info.drop(columns=['clean_name', 'state_clean', 'Bank Asset Size Raw'], inplace=True)

# Save result
output_path = 'bank_info_with_asset_size_final.xlsx'
bank_info.to_excel(output_path, index=False)

print("✅ Strict match complete! Output saved to:", output_path)
