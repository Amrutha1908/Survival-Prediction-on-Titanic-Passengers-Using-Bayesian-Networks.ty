Step 1: Data Understanding and Preprocessing
import pandas as pd
# Load the dataset file_path = "C:\\Users\\Amurtha\\Downloads\\Titanic dataset.csv" df = pd.read_csv(file_path)
# Explore the dataset print(df.head()) print(df.info()) print(df.describe())
# Handle missing values df.fillna(method='ffill', inplace=True)
# Feature engineering # Convert categorical variables to numerical df['Sex'] = df['Sex'].map({'male': 0, 'female': 1}) df['Embarked'] = df['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})
# Drop irrelevant columns df.drop(['Name', 'Ticket', 'Cabin'], axis=1, inplace=True)
# Split the data into training and testing sets from sklearn.model_selection import train_test_split
X = df.drop('Survived', axis=1) y = df['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    50%    1100.500000    0.000000    3.000000   27.000000    0.000000   75%    1204.750000    1.000000    3.000000   39.000000    1.000000   max    1309.000000    1.000000    3.000000   76.000000    8.000000   
            Parch        Fare  count  418.000000  417.000000  mean     0.392344   35.627188  std      0.981429   55.907576  min      0.000000    0.000000  25%      0.000000    7.895800  
50%      0.000000   14.454200    
        
Step 2: Bayesian Network
                 
from pgmpy.models import BayesianNetwork from pgmpy.estimators import MaximumLikelihoodEstimator
# Define the structure of the Bayesian Network model = BayesianNetwork([('Pclass', 'Survived'),                          ('Sex', 'Survived'),
                         ('Age', 'Survived'),
                         ('Fare', 'Survived'),
                         ('Embarked', 'Survived'),
                         ('Parch', 'Survived'),                          ('SibSp', 'Survived')])
# Fit the model model.fit(df, estimator=MaximumLikelihoodEstimator)
# Inferencing from pgmpy.inference import VariableElimination
infer = VariableElimination(model) q = infer.map_query(variables=['Survived'], evidence={'Pclass': 1, 'Sex': 1}) print(q)
  Finding Elimination Order: : 100%|██████████| 5/5 [00:00<00:00, 66.87it/s]
Eliminating: Embarked: 100%|██████████| 5/5 [00:00<00:00, 65.02it/s]{'Survived': 1} Step 4: Latent Dirichlet Allocation (LDA)
from sklearn.decomposition import LatentDirichletAllocation from sklearn.feature_extraction.text import CountVectorizer
# Text data preprocessing df['Name'] = df['Name'].fillna('')
# Vectorize the 'Name' field
vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
X_text = vectorizer.fit_transform(df['Name'])
# Fit the LDA model lda = LatentDirichletAllocation(n_components=5, random_state=42) lda.fit(X_text)
# Display topics for idx, topic in enumerate(lda.components_):
    print(f"Topic {idx}:")
    print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-11:-1]])
  Topic 0:
['mr', 'william', 'mrs', 'george', 'john', 'edward', 'alice', 'sage', 'ware', 'joseph'] Topic 1:
['mr', 'john', 'thomas', 'henry', 'james', 'johan', 'alfred', 'samuel', 'albert', 'harry'] Topic 2:
['miss', 'mr', 'charles', 'patrick', 'frederick', 'maria', 'edith', 'frank', 'august', 'abraham'] Topic 3:
['mrs', 'arthur', 'alexander', 'mary', 'bridget', 'frank', 'henry', 'john', 'elizabeth', 'james'] Topic 4:
['master', 'miss', 'joseph', 'mrs', 'elizabeth', 'john', 'mary', 'asplund', 'walter', 'ida']
