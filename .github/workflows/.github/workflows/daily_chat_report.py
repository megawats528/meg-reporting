"""
return summaries


# ---------- Report builder ----------


def build_markdown_report(summaries):
today = dt.date.today().isoformat()
lines = [f"# Daily Chat Themes — {today}\n", f"_Generated: {dt.datetime.utcnow().isoformat()} UTC_\n", "## Executive summary\n"]
lines.append(f"- Total clusters detected: {len(summaries)}\n")
lines.append("## Themes & Insights\n")
for s in summaries:
title = s.get('title', s['top_words'].split(',')[0])
lines.append(f"### Theme {s['topic_id']}: {title}\n")
lines.append(f"- **Count:** {s['count']}\n")
if s.get('insight'):
lines.append(f"- **Insight:** {s['insight']}\n")
if s.get('action'):
lines.append(f"- **Recommended action:** {s['action']}\n")
lines.append(f"- **Top words:** {s['top_words']}\n")
lines.append("- **Examples:**\n")
for ex in s['examples']:
lines.append(f" - {ex}\n")
lines.append("\n")
return "\n".join(lines)


# ---------- Slack helper ----------
def post_to_slack(summary_md, slack_token, channel):
from slack_sdk import WebClient
client = WebClient(token=slack_token)
# post top 8 lines as a short message
text = '\n'.join(summary_md.splitlines()[:40])
client.chat_postMessage(channel=channel, text=text)


# ---------- Main ----------


def main():
INPUT = Path('./input')
OUTPUT = Path('./output')
OUTPUT.mkdir(parents=True, exist_ok=True)


df = load_latest_trace(INPUT)
if df.empty:
print('No input traces found in ./input — exiting')
return
df = normalize_df(df)
messages = df['message'].tolist()
if not messages:
print('No messages after normalization — exiting')
return


embeddings = build_embeddings(messages)
topic_model, topics, probs = cluster_messages(messages, embeddings, min_topic_size=int(os.getenv('MIN_TOPIC_SIZE', '20')))
summaries = summarize_topics(topic_model, messages, topics)


# optional LLM polishing
openai_key = os.getenv('OPENAI_API_KEY')
if openai_key:
for s in summaries:
try:
out = call_llm_for_insight(s, openai_key, model_name=os.getenv('LLM_MODEL', 'gpt-4o-mini'))
parsed = json.loads(out)
s.update(parsed)
except Exception as e:
s['title'] = s.get('top_words').split(',')[0]


md = build_markdown_report(summaries)
fname = OUTPUT / f"daily_chat_report_{dt.date.today().isoformat()}.md"
fname.write_text(md, encoding='utf-8')
print('Wrote:', fname)


# optional Slack
slack_token = os.getenv('SLACK_BOT_TOKEN')
slack_chan = os.getenv('SLACK_CHANNEL')
if slack_token and slack_chan:
try:
post_to_slack(md, slack_token, slack_chan)
print('Posted summary to Slack')
except Exception as e:
print('Slack post failed:', e)


if __name__ == '__main__':
main()
