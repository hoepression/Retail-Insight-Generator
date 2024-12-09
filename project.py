from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_google_genai import GoogleGenerativeAI

from few_shots import few_shots
import os
from dotenv import load_dotenv
load_dotenv() # take environment variables from .env (especially openai api key) Obtain a api and declare them in a seperate .env file


def get_few_shot_db_chain():
llm = GoogleGenerativeAI(google_api_key=os.environ[&quot;GOOGLE_API_KEY&quot;], model=&quot;gemini-pro&quot;,
temperature=0.1)
db_user = &quot;root&quot;
db_password = &quot;chinnu&quot;
db_host = &quot;localhost&quot;
db_name = &quot;atliq_tshirts&quot;
db = SQLDatabase.from_uri(f&quot;mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}&quot;,
sample_rows_in_table_info=3)
embeddings = SentenceTransformerEmbeddings(model_name=&#39;sentence-transformers/all-MiniLM-L6-
v2&#39;)
to_vectorize = [&quot; &quot;.join(example.values()) for example in few_shots]
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
example_selector = SemanticSimilarityExampleSelector(
vectorstore=vectorstore,
k=2,
)

mysql_prompt = &quot;&quot;&quot;You are a MySQL expert. Given an input question, first create a syntactically correct
MySQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most
{top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most
informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer
the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query
for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves &quot;today&quot;.
Use the following format:
Question: Question here
SQLQuery: Query to run with no pre-amble
SQLResult: Result of the SQLQuery
Answer: Final answer here
No pre-amble.
&quot;&quot;&quot;
example_prompt = PromptTemplate(
input_variables=[&quot;Question&quot;, &quot;SQLQuery&quot;, &quot;SQLResult&quot;, &quot;Answer&quot;, ],
template=&quot;\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer:
{Answer}&quot;,
)
few_shot_prompt = FewShotPromptTemplate(
example_selector=example_selector,
example_prompt=example_prompt,
prefix=mysql_prompt,
suffix=PROMPT_SUFFIX,
input_variables=[&quot;input&quot;, &quot;table_info&quot;, &quot;top_k&quot;], # These variables are used in the prefix and suffix
)
chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
return chain
if __name__==&quot;__main__&quot;:
chain=get_few_shot_db_chain()
print(chain.invoke(&quot;How many Nike t-shirts are there in stock?&quot;))
