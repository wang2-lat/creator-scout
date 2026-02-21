# Creator Scout

CLI tool to discover and manage micro-influencer partnerships for better conversion.

## Installation


## Usage

### Add a creator

### Search creators

### List all creators

### Analyze creator

### Create partnership

### View partnerships

### Update ROI

## Features

- Search creators by platform, niche, and follower count
- Analyze engagement rates and performance metrics
- Track partnership status and progress
- Calculate ROI on influencer campaigns
- SQLite database for local data storage

## Commands

- `add` - Add new creator to database
- `search` - Search creators with filters
- `list-creators` - List all creators
- `analyze` - Analyze creator metrics
- `partner` - Create partnership record
- `partnerships` - View all partnerships
- `update-roi` - Update partnership ROI
pip install -r requirements.txt
python main.py add "Tech Reviewer" youtube tech 80000 5.2
python main.py search --platform youtube --min-followers 50000
python main.py analyze 1
python main.py partner 1 --budget 3000 --status negotiating