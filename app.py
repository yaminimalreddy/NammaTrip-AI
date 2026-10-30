import os, json, re
import streamlit as st
import requests

st.set_page_config(page_title='NammaTrip AI | Karnataka Travel Planner',page_icon='🌿',layout='wide')
st.markdown('''<style>.stApp{background:#f6f8f5;color:#17352b}.hero{padding:2rem;border-radius:22px;background:linear-gradient(110deg,#123d30,#34765a);color:white}.hero h1{font-size:3rem;margin:0}.stButton>button{background:#236b4d;color:white;border-radius:12px}</style>''',unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🌿 NammaTrip AI</h1><p>Discover Karnataka, your way. Thoughtful journeys, tailored to you.</p></div>',unsafe_allow_html=True)
st.write('')
with st.sidebar:
 st.header('Plan your escape')
 origin=st.selectbox('Starting city',['Bengaluru','Mysuru','Mangaluru','Hubballi','Belagavi','Other'])
 if origin=='Other': origin=st.text_input('Enter starting city','Bengaluru')
 days=st.slider('Trip duration (days)',1,10,3)
 budget=st.number_input('Total trip budget (₹)',min_value=1000,max_value=500000,value=10000,step=500)
 travelers=st.number_input('Number of travellers',1,20,2)
 interests=st.multiselect('Your interests',['Nature','Waterfalls','Beaches','Heritage','Wildlife','Adventure','Food','Spirituality','Coffee estates'],default=['Nature','Heritage'])
 vibe=st.selectbox('Travel style',['Relaxed','Balanced','Packed','Family-friendly','Romantic','Adventure'])
 transport=st.selectbox('Preferred transport',['Public transport','Car','Bike','Flexible'])

DESTINATIONS=[{'name':'Coorg (Kodagu)','interests':['Nature','Waterfalls','Coffee estates','Adventure'],'highlights':['Abbey Falls','Raja’s Seat','Dubare Elephant Camp']},{'name':'Mysuru','interests':['Heritage','Food','Spirituality'],'highlights':['Mysore Palace','Chamundi Hills','Devaraja Market']},{'name':'Hampi','interests':['Heritage','Adventure'],'highlights':['Virupaksha Temple','Stone Chariot','Matanga Hill']},{'name':'Chikkamagaluru','interests':['Nature','Coffee estates','Adventure','Waterfalls'],'highlights':['Mullayanagiri','Hirekolale Lake','Coffee estate trails']},{'name':'Gokarna','interests':['Beaches','Spirituality','Nature'],'highlights':['Om Beach','Kudle Beach','Mahabaleshwar Temple']},{'name':'Udupi','interests':['Beaches','Food','Spirituality'],'highlights':['Malpe Beach','Sri Krishna Temple','St Mary’s Island']},{'name':'Kabini','interests':['Wildlife','Nature'],'highlights':['Kabini backwaters','Wildlife safari (subject to availability)']},{'name':'Badami','interests':['Heritage','Adventure'],'highlights':['Cave temples','Agastya Lake','Bhutanatha temples']}]

def local_plan():
 ranked=sorted(DESTINATIONS,key=lambda x:sum(i in x['interests'] for i in interests),reverse=True)
 picks=ranked[:min(2,max(1,(days+2)//3))]
 allocation={'Transport':round(budget*.30),'Stay':round(budget*.35),'Food':round(budget*.20),'Activities & buffer':budget-round(budget*.30)-round(budget*.35)-round(budget*.20)}
 itinerary=[]
 for d in range(days):
  place=picks[min(len(picks)-1,d*len(picks)//days)]
  itinerary.append({'day':d+1,'destination':place['name'],'morning':place['highlights'][0],'afternoon':place['highlights'][min(1,len(place['highlights'])-1)],'evening':place['highlights'][-1],'note':'Check opening hours, travel time, tickets and local conditions before visiting.'})
 return {'title':f'{days}-day Karnataka escape','summary':f'A {vibe.lower()} trip from {origin} for {travelers} traveller(s), focused on {", ".join(interests) or "Karnataka highlights"}.','itinerary':itinerary,'budget_breakdown':allocation,'tips':['Budget is a planning allocation, not verified live prices.','Check travel distances and accommodation availability before booking.']}

def get_setting(name, default=''):
 # Read Streamlit secrets only when a secrets file exists; otherwise use environment variables.
 value = os.getenv(name, default)
 try:
  secrets_file = os.path.join(os.getcwd(), '.streamlit', 'secrets.toml')
  if os.path.exists(secrets_file):
   value = st.secrets.get(name, value)
 except Exception:
  pass
 return value

def ai_plan():
 key=get_setting('GEMINI_API_KEY','')
 if not key:return None,'Gemini API key is not configured. Using the built-in Karnataka itinerary generator.' 
 prompt=f'''You are a careful Karnataka travel planner. Return ONLY valid JSON with keys title (string), summary (string), itinerary (array of objects with day integer, destination, morning, afternoon, evening, note strings), budget_breakdown (object with numeric Transport, Stay, Food, Activities & buffer), tips (array of strings). Create EXACTLY {days} days. Origin: {origin}. Total budget INR {budget} for {travelers} travellers. Interests: {interests}. Style: {vibe}. Transport: {transport}. Budget categories must sum exactly to {budget}. Avoid fabricated live prices, opening times, travel times or booking availability. Mention that estimates need verification. Keep all destinations in Karnataka. Be realistic about intercity travel.'''
 try:
  model=get_setting('GEMINI_MODEL','gemini-2.5-flash')
  url=f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
  response=requests.post(url,params={'key':key},json={'contents':[{'parts':[{'text':prompt}]}],'generationConfig':{'responseMimeType':'application/json','temperature':0.4}},timeout=45)
  response.raise_for_status()
  raw=response.json()['candidates'][0]['content']['parts'][0]['text']
  data=json.loads(raw)
  if len(data['itinerary'])!=days:raise ValueError('Unexpected day count')
  return data,None
 except Exception as e:return None,f'AI unavailable ({str(e)[:140]}). Showing an offline itinerary.'

st.subheader('Your journey starts here')
st.caption('Personalized routes • Flexible budgets • Karnataka-focused discovery')
if st.button('✨ Generate my itinerary',type='primary',use_container_width=True):
 with st.spinner('Designing your trip...'):
  plan,warning=ai_plan()
  if warning:st.warning(warning)
  if plan is None:plan=local_plan()
  st.session_state['plan']=plan
if 'plan' in st.session_state:
 p=st.session_state['plan'];st.header(p['title']);st.write(p['summary'])
 c1,c2,c3=st.columns(3);c1.metric('Duration',f'{days} days');c2.metric('Total budget',f'₹{budget:,}');c3.metric('Travellers',travelers)
 st.subheader('Day-by-day itinerary')
 for day in p['itinerary']:
  with st.expander(f"Day {day['day']} — {day['destination']}",expanded=True):
   st.write('🌅 **Morning:**',day['morning']);st.write('☀️ **Afternoon:**',day['afternoon']);st.write('🌙 **Evening:**',day['evening']);st.caption(day.get('note',''))
 st.subheader('Suggested budget allocation')
 st.bar_chart(p['budget_breakdown'])
 st.write('**Travel tips**')
 for tip in p.get('tips',[]):st.write('•',tip)
 st.download_button('⬇️ Download itinerary (JSON)',json.dumps(p,ensure_ascii=False,indent=2),file_name='nammatrip_itinerary.json',mime='application/json')
st.divider();st.caption('NammaTrip AI • Estimates are illustrative; verify transport, prices, safety and opening hours before travel.')
