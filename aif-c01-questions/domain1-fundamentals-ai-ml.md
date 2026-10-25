# Domain 1: Fundamentals of AI and ML (20%)

Guide page: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain1.html>

---

## Task 1.1: Explain basic AI concepts and terminologies

**1.** A product manager is preparing a slide that explains how the terms used by the data science team relate to each other. Which statement correctly describes the relationship between artificial intelligence (AI), machine learning (ML), deep learning, and generative AI?
- A. AI contains ML, ML contains deep learning, and generative AI is built mostly on deep learning models
- B. Deep learning is the broadest field, and AI, ML, and generative AI are separate techniques inside it
- C. ML and AI are two names for the same field, and deep learning is an unrelated statistics discipline
- D. Generative AI contains ML, and AI is a subset of ML that only applies to rule-based expert systems

<details><summary>Answer</summary>

**A.** AI is the broad field of making machines perform tasks that need human-like intelligence. ML is the subset of AI that learns patterns from data. Deep learning is the subset of ML that uses multi-layer neural networks, and modern generative AI models (such as transformer-based LLMs and diffusion models) are deep learning models.

Why not the others:
- **B.** Deep learning is one of the narrowest of these terms, not the broadest. It's a family of ML methods based on neural networks.
- **C.** ML is a subset of AI, not a synonym, and deep learning is a branch of ML rather than an unrelated discipline.
- **D.** This reverses the hierarchy. AI is the outermost field, and rule-based expert systems are one kind of AI that doesn't involve learning from data.

Resource: <https://aws.amazon.com/what-is/deep-learning/>
</details>

**2.** A travel company already has a generative AI chatbot that answers questions about its destinations. The company now wants an assistant that can take a request such as "rebook my cancelled flight and update my hotel," break it into steps, call the airline and hotel booking APIs, check the results, and keep going until the task is done. Which term BEST describes this new assistant?
- A. A supervised classification model that labels each request with one of several predefined travel categories
- B. A rule-based expert system that follows a fixed decision tree written by the company's travel agents
- C. A diffusion model that generates new itineraries by gradually removing noise from random input data
- D. An agentic AI system that plans multi-step tasks and uses tools to act toward a goal with limited supervision

<details><summary>Answer</summary>

**D.** Agentic AI goes beyond generating a response: an agent reasons about a goal, plans steps, calls tools or APIs, observes the results, and iterates with limited human supervision. A chatbot that only answers questions is generative AI; one that acts on the customer's behalf across systems is agentic.

Why not the others:
- **A.** A classifier only assigns a label to the request. It doesn't plan steps or call booking APIs to complete the task.
- **B.** A fixed decision tree can't adapt to the many combinations of cancellations, rebookings and hotel changes the way a reasoning agent can.
- **C.** Diffusion models generate media such as images by denoising. They don't orchestrate API calls to complete a workflow.

Resource: <https://aws.amazon.com/what-is/agentic-ai/>
</details>

**3. (Matching)** A data science team supports several applications with different inference needs. Match each requirement to the type of inference that fits it BEST.
- Score 40 million customer records once a night and write the results to Amazon S3 => Batch inference
- Return a fraud decision within 100 milliseconds while a card payment is being authorized => Real-time inference
- Process uploaded 500 MB medical images that each take several minutes to analyze, queuing requests during spikes => Asynchronous inference
- Serve an internal tool that receives a few requests a day, where occasional cold-start delays are acceptable => Serverless inference

<details><summary>Answer</summary>

Batch inference processes a large dataset offline with no persistent endpoint. Real-time inference keeps an endpoint running for low-latency, interactive requests. Asynchronous inference queues requests with large payloads or long processing times and returns results later (SageMaker AI asynchronous endpoints can scale to zero when the queue is empty). Serverless inference provisions compute only when requests arrive, which suits intermittent traffic that can tolerate cold starts.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html>
</details>

**4.** A radiology startup hosts a computer vision model on Amazon SageMaker AI. Each request uploads a scan of up to 800 MB, and the model takes up to 10 minutes to produce a result. Requests arrive in unpredictable bursts, and the company doesn't want to pay for idle instances overnight. Which deployment option should it use?
- A. A real-time endpoint with a large GPU instance that stays running at all times to keep latency low
- B. An asynchronous inference endpoint that queues requests, supports large payloads, and can scale to zero
- C. A batch transform job that runs once a day over all scans uploaded during the previous 24 hours
- D. A serverless endpoint, because it accepts payloads of any size and has no limit on processing time

<details><summary>Answer</summary>

**B.** SageMaker AI asynchronous inference queues incoming requests, supports payloads up to 1 GB and processing times up to one hour, and can scale the instance count to zero when there are no requests, so the startup doesn't pay for idle capacity.

```arch
users: users Clinicians
cloud AWS Cloud
  s3in: s3 S3 bucket | uploaded scans
  ep: sagemaker *Async endpoint | internal queue, scales to zero
  s3out: s3 S3 bucket | results
  sns: sns Amazon SNS
---
1. users -> s3in : upload scan
2. s3in -> ep : queued request
3. ep -> s3out : write result
4. ep ~> sns : done notification
```

Why not the others:
- **A.** An always-on real-time endpoint pays for idle GPU capacity overnight, and real-time endpoints have small payload and short timeout limits that don't fit 800 MB, 10-minute requests.
- **C.** A once-a-day batch job would make clinicians wait up to a day for results, and the bursts call for processing as requests arrive.
- **D.** Serverless endpoints have small payload limits and short maximum processing times, so they can't handle 800 MB scans that take minutes.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html>
</details>

**5.** A human resources team built a model that answers policy questions for a small internal tool. Traffic is very low and unpredictable — sometimes nothing for days — and employees don't mind if the first answer after a quiet period takes a few extra seconds. Which SageMaker AI inference option is MOST cost-effective?
- A. A real-time endpoint on a GPU instance that runs continuously so every request is fast
- B. A batch transform job that runs every hour and stores answers for questions employees might ask
- C. Serverless inference, which provisions compute only when requests arrive and bills for the compute used
- D. A multi-node training cluster that stays running so the model can be retrained on every request

<details><summary>Answer</summary>

**C.** Serverless inference automatically launches compute when requests arrive and scales down when traffic stops, so the team pays only while requests are processed. The trade-off is a cold-start delay after idle periods, which this team accepts.

Why not the others:
- **A.** A continuously running GPU instance would sit idle for days at a time and cost far more than this traffic justifies.
- **B.** Batch transform scores a dataset offline. It can't answer an employee's new question on demand.
- **D.** Training clusters are for building models, not serving answers, and retraining per request makes no sense here.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html>
</details>

**6.** An insurance company wants to score its entire policy database of 12 million rows once a month to estimate each customer's renewal likelihood. Nobody needs a response in real time, and the company doesn't want an endpoint running between monthly runs. Which approach should it use?
- A. Deploy a real-time endpoint and call it 12 million times from a loop on a laptop
- B. Use SageMaker AI batch transform to run inference over the dataset in Amazon S3
- C. Configure a serverless endpoint and wait for customers to trigger each prediction themselves
- D. Ask an Amazon Lex bot to collect each customer's details and predict renewal during a chat

<details><summary>Answer</summary>

**B.** Batch transform runs inference over an entire dataset stored in S3, writes the predictions back to S3, and releases the compute when the job finishes. It's designed for large, offline, scheduled scoring with no persistent endpoint.

Why not the others:
- **A.** A real-time endpoint is built for low-latency single requests. Keeping it up and looping through millions of rows is slower to manage and pays for an endpoint that isn't needed.
- **C.** The company needs predictions for every policy, not only for customers who happen to make a request.
- **D.** Lex builds conversational interfaces. It isn't a way to score a database of existing records.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html>
</details>

**7.** A retailer has five years of past transactions in which each record is marked "returned" or "kept." It wants a model that predicts whether a new order will be returned. What does the "returned/kept" field represent, and which kind of learning does it enable?
- A. It is a label (the known outcome) that makes the data suitable for supervised learning
- B. It is a feature that should be removed so the model can learn without bias in an unsupervised way
- C. It is a reward signal that lets an agent learn by trial and error through reinforcement learning
- D. It is an embedding that groups similar orders together so the model can cluster them automatically

<details><summary>Answer</summary>

**A.** A label is the known answer attached to each training example. Labeled data lets a supervised learning algorithm learn the mapping from inputs (order details) to the outcome (returned or kept) and then predict the outcome for new orders.

Why not the others:
- **B.** The outcome field is the target the model must predict. Removing it would leave nothing for the model to learn to predict.
- **C.** Reinforcement learning learns from rewards received while interacting with an environment, not from a historical table of known outcomes.
- **D.** Embeddings are numerical representations of data, and clustering is unsupervised. A known outcome column is a label, not an embedding.

Resource: <https://aws.amazon.com/what-is/supervised-learning/>
</details>

**8.** A data team is cataloging the datasets it could use for ML projects. Which TWO datasets are examples of structured data? (Select TWO.)
- A. A table of loan applications with columns for income, loan amount, and credit score
- B. A folder of recorded customer service phone calls stored as MP3 files
- C. Hourly electricity-meter readings stored as timestamp and kilowatt-hour columns
- D. A collection of scanned handwritten letters saved as JPEG images
- E. Free-text product reviews copied from the company's website

<details><summary>Answer</summary>

**A, C.** Structured data follows a fixed schema of rows and columns, like a database table. Tabular loan data is structured, and so is time-series meter data stored as timestamp and value columns. Audio, images, and free text are unstructured: they have no predefined fields, so ML models need techniques such as speech recognition, computer vision or NLP to use them.

Why not the others:
- **B.** Audio recordings are unstructured data. They must be transcribed or otherwise processed before their content fits into fields.
- **D.** Images are unstructured data. Extracting the text would need OCR or a service like Amazon Textract.
- **E.** Free-text reviews are unstructured. Their meaning has to be extracted with NLP, for example with Amazon Comprehend.

Resource: <https://aws.amazon.com/what-is/machine-learning/>
</details>

**9. (Matching)** A training course asks learners to identify the type of machine learning each scenario uses. Match each scenario to the learning type.
- Predict next month's sales from historical sales figures that include the actual results => Supervised learning
- Group website visitors into segments based on browsing behavior, with no predefined segments => Unsupervised learning
- Teach a warehouse robot to pick items by rewarding successful grasps and penalizing drops => Reinforcement learning
- Flag unusual network traffic patterns when no examples of attacks have been labeled => Unsupervised learning
- Classify support emails as "billing" or "technical" using thousands of emails already tagged by agents => Supervised learning

<details><summary>Answer</summary>

Supervised learning trains on labeled examples (known sales figures, tagged emails). Unsupervised learning finds structure in unlabeled data, such as clusters of similar visitors or anomalies that don't fit normal patterns. Reinforcement learning trains an agent through trial and error, using rewards and penalties from its environment.

Resource: <https://aws.amazon.com/what-is/reinforcement-learning/>
</details>

**10.** A logistics company wants software that learns how to route delivery drones through a simulated city. There is no dataset of "correct" routes. Instead, the simulation gives positive points for fast, safe deliveries and negative points for collisions or wasted battery. Which learning approach fits this problem?
- A. Supervised learning, because the simulation's points are labels attached to a fixed set of example routes
- B. Unsupervised learning, because the model groups similar routes together without any feedback at all
- C. Reinforcement learning, because an agent learns a policy by acting and receiving rewards or penalties
- D. Transfer learning, because the drones copy the routes that a pre-trained language model already knows

<details><summary>Answer</summary>

**C.** In reinforcement learning, an agent takes actions in an environment, receives rewards or penalties, and gradually learns a policy that maximizes total reward. A simulator that scores each flight is a classic reinforcement learning setup.

Why not the others:
- **A.** There is no labeled dataset of correct routes. The points come from the agent's own actions as it explores, which is reinforcement learning, not supervised learning.
- **B.** Unsupervised learning finds patterns without feedback. Here the rewards are feedback that drives learning.
- **D.** Transfer learning reuses knowledge from a model trained on a related task. A language model has no knowledge of drone routes to transfer.

Resource: <https://aws.amazon.com/what-is/reinforcement-learning/>
</details>

**11.** A model that predicts equipment failures scores 99% accuracy on its training data but only 62% on new data from the factory floor. What is the MOST likely problem?
- A. The model is underfitting, because it is too simple to capture the patterns in the training data
- B. The model has low variance, because its predictions barely change between datasets
- C. The model is well fit, because training accuracy is the only metric that matters for production
- D. The model is overfitting, because it memorized noise in the training data and doesn't generalize

<details><summary>Answer</summary>

**D.** Overfitting happens when a model learns the training data too closely, including its noise, so it performs very well on training data but poorly on unseen data. A large gap between training and test performance is the classic sign. Fixes include more or more varied data, regularization, simpler models, or early stopping.

Why not the others:
- **A.** An underfit model performs poorly on the training data too. Here training accuracy is very high.
- **B.** Overfit models have high variance: their behavior depends heavily on the particular training data, which is why they fail on new data.
- **C.** Performance on new, unseen data is what matters in production. A large drop shows the model doesn't generalize.

Resource: <https://aws.amazon.com/what-is/overfitting/>
</details>

**12.** A team trains a straight-line model to predict ride-share demand, which rises and falls sharply with time of day, weather, and events. The model performs poorly on both the training data and the test data. Which term describes this situation?
- A. Underfitting, caused by a model too simple to capture the real patterns in the data
- B. Overfitting, caused by the model memorizing every training example perfectly
- C. Data leakage, caused by the test set accidentally containing the training labels
- D. Hallucination, caused by the model inventing demand figures that look plausible

<details><summary>Answer</summary>

**A.** Underfitting means the model is too simple (high bias) to capture the relationships in the data, so it performs poorly even on the data it was trained on. More expressive models, better features, or longer training can help.

Why not the others:
- **B.** An overfit model scores very well on training data. Poor training performance points to underfitting.
- **C.** Leakage usually makes test results look unrealistically good, not poor across the board.
- **D.** Hallucination describes generative models producing confident but false content. It isn't the term for a regression model that's too simple.

Resource: <https://docs.aws.amazon.com/machine-learning/latest/dg/model-fit-underfitting-vs-overfitting.html>
</details>

**13.** A new analyst asks why the ML team's GPU bill was high last month but is much lower now, even though the model is used by thousands of customers every day. Which explanation is MOST accurate?
- A. Inference builds the model from scratch for every request, while training only formats the input data for the model
- B. Training and inference are the same process, so the cost difference must come from storage charges
- C. Training learns model parameters from data and is compute-heavy; inference uses the model to predict
- D. Inference requires labeled data for every request, while training can run on unlabeled data only

<details><summary>Answer</summary>

**C.** Training is the process of learning model parameters from (often large) datasets, which typically needs heavy compute for a period of time. Inference is using the finished model to make predictions on new inputs, which is usually much cheaper per request, although its total cost grows with traffic.

Why not the others:
- **A.** This reverses the two. Inference doesn't rebuild the model; it uses the parameters learned during training.
- **B.** Training and inference are distinct phases with different compute patterns. A finished training phase explains the drop.
- **D.** Inference inputs don't need labels; the model predicts them. Labels are needed for supervised training.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-mlconcepts.html>
</details>

**14.** A wildlife charity has 2 million camera-trap photos and wants a model that recognizes which animal species appears in each one. A consultant recommends a deep learning model. Why is deep learning a good fit for this task?
- A. Deep learning is the only approach that works without any training data, so no photos need labels
- B. Deep learning models are always fully explainable, which the charity's donors require
- C. Deep learning is a rules engine that lets biologists write an if/then statement for each species
- D. Multi-layer neural networks learn useful features directly from raw pixels in large unstructured datasets

<details><summary>Answer</summary>

**D.** Deep learning uses neural networks with many layers that learn increasingly complex features (edges, textures, shapes, animals) directly from raw unstructured data such as images, without hand-engineered features. With a large photo collection, it's the standard approach for computer vision.

Why not the others:
- **A.** Species recognition still needs labeled examples (or a pre-trained model to fine-tune). Deep learning usually needs more data, not less.
- **B.** Deep neural networks are generally harder to explain than simpler models such as linear models or decision trees.
- **C.** Deep learning learns patterns from data; it isn't a hand-written rules engine.

Resource: <https://aws.amazon.com/what-is/neural-network/>
</details>

**15.** A city government is reviewing proposed AI projects. Which TWO projects are examples of natural language processing (NLP)? (Select TWO.)
- A. Counting cars in traffic-camera video to adjust signal timing at busy intersections
- B. Detecting the sentiment and key complaints in thousands of resident feedback emails
- C. Reading license plates from parking-garage images to automate billing
- D. Translating council meeting summaries from English into Spanish and Vietnamese
- E. Forecasting next summer's water usage from ten years of daily meter readings

<details><summary>Answer</summary>

**B, D.** NLP is the branch of AI that understands and generates human language. Sentiment analysis of text and machine translation are both NLP tasks (on AWS, Amazon Comprehend and Amazon Translate).

Why not the others:
- **A.** Counting cars in video is computer vision, which interprets images and video.
- **C.** Reading plates from images is computer vision (optical character recognition), even though the output is text.
- **E.** Forecasting from numeric time-series data is a regression/forecasting task, not language processing.

Resource: <https://aws.amazon.com/what-is/nlp/>
</details>

**16.** A marketing director asks what a large language model (LLM) actually is. Which description is MOST accurate?
- A. A database that stores every sentence on the internet and returns the closest match to a question
- B. A very large transformer-based deep learning model pre-trained on huge text data
- C. A rule-based program in which linguists hand-code grammar rules for each supported language
- D. A small statistical model trained on one company's data that can only classify text into categories

<details><summary>Answer</summary>

**B.** An LLM is a deep learning model with billions of parameters, typically based on the transformer architecture, pre-trained on vast amounts of text to predict the next token. That pre-training lets it generate text, answer questions, summarize, translate and more, often without task-specific training.

Why not the others:
- **A.** LLMs don't store and look up sentences. They learn statistical patterns in their parameters and generate new text token by token.
- **C.** LLMs learn language patterns from data rather than following hand-written grammar rules.
- **D.** LLMs are large, general-purpose models pre-trained on broad data, not small single-purpose classifiers.

Resource: <https://aws.amazon.com/what-is/large-language-model/>
</details>

**17.** A bank's loan-approval model approves applicants from one postal region far less often than equally qualified applicants elsewhere. An investigation finds that the training data came mostly from branches outside that region. Which term BEST describes this problem?
- A. Latency, because the model takes longer to respond for applicants from that region
- B. Hallucination, because the model invents applicant details that aren't in the data
- C. Inference, because the model is being used on new applications after training
- D. Bias, because skewed training data makes the model treat a group of people unfairly

<details><summary>Answer</summary>

**D.** Bias in ML is a systematic error that leads to unfair outcomes for certain groups, often because the training data under-represents or misrepresents them. Fairness means the model's outcomes don't unjustly disadvantage particular groups.

Why not the others:
- **A.** Latency is about response time. The problem is about who gets approved, not how fast.
- **B.** Hallucination refers to generative models producing false content. A loan model approving fewer qualified applicants is bias.
- **C.** Inference is simply using a trained model. It describes when the problem shows up, not what the problem is.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-data-bias.html>
</details>

## Task 1.2: Identify practical use cases for AI

**18.** A payroll company must calculate statutory tax withholding for every paycheck. The rules are published by the government, change once a year, and must produce exactly the same result for the same inputs every time. A team member proposes training an ML model on past paychecks to predict withholding amounts. What is the BEST response?
- A. Implement the published rules in conventional code, because the task needs an exact, deterministic outcome
- B. Train a deep learning model, because neural networks are more accurate than any written rule
- C. Use a generative AI model, because it can read the tax rules and produce slightly different answers
- D. Collect more paycheck data first, because ML always outperforms rules once the dataset is large enough

<details><summary>Answer</summary>

**A.** ML produces probabilistic predictions learned from data. When a task has known, fixed rules and requires an exact, repeatable result, deterministic code is cheaper, auditable, and correct by design. AI/ML isn't the right tool when a specific outcome is required instead of a prediction.

Why not the others:
- **B.** A neural network would approximate the rules and could be wrong for some inputs, which isn't acceptable for statutory calculations.
- **C.** Nondeterministic output is exactly what payroll can't tolerate. Generative models can vary their answers for the same input.
- **D.** More data doesn't change the fact that a prediction can be wrong while the published rule is exact.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html>
</details>

**19.** A small bakery with one location asks a consultant whether to build an ML model to predict how many croissants to bake each morning. It has three months of sales records, sells about the same amount daily, and the owner already estimates within a few croissants. What should the consultant conclude?
- A. ML is always worth it, because any prediction task benefits from a custom model
- B. The bakery should pre-train its own foundation model on its sales records to improve forecasts
- C. A custom ML model probably isn't worth the cost here; the benefit is small compared with the effort
- D. The bakery should use reinforcement learning so the model can experiment by baking extra batches

<details><summary>Answer</summary>

**C.** A cost-benefit analysis should come before any ML project. With little data, stable demand, and an owner who already estimates accurately, the cost of building and maintaining a model would outweigh the small improvement it could deliver.

Why not the others:
- **A.** ML adds value when the problem is complex, data is available, and the payoff justifies the cost. That isn't the case for every prediction.
- **B.** Pre-training a foundation model costs far more than the bakery's entire problem is worth, and three months of sales records is nowhere near enough data.
- **D.** Experimenting by baking extra batches would waste product and money for a problem the owner already handles well.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html>
</details>

**20.** A real estate website wants to show an estimated sale price, in dollars, for every listed home based on its size, location, age, and number of bedrooms. Which ML technique fits this use case?
- A. Binary classification, because the model predicts whether a house will sell
- B. Regression, because the model predicts a continuous numeric value
- C. Clustering, because the model groups houses into segments without labels
- D. Reinforcement learning, because the model learns by negotiating with buyers

<details><summary>Answer</summary>

**B.** Regression predicts a continuous numeric value, such as a price, from input features. Historical sale prices serve as the labels.

Why not the others:
- **A.** Classification predicts a category (sold / not sold). The website needs a dollar amount.
- **C.** Clustering groups similar items without labels. It doesn't output a price estimate.
- **D.** Reinforcement learning learns from rewards through interaction. Estimating prices from historical sales is a supervised regression problem.

Resource: <https://aws.amazon.com/what-is/supervised-learning/>
</details>

**21.** An online retailer has purchase histories for 3 million customers but no predefined customer categories. The marketing team wants to discover natural groups of customers with similar buying behavior so it can design a campaign for each group. Which technique should the team use?
- A. Clustering, an unsupervised technique that groups similar customers without labels
- B. Regression, to predict each customer's exact lifetime spending in dollars
- C. Multi-class classification, to assign customers to segments the team defined in advance
- D. Text generation, to write a description of every customer with a large language model

<details><summary>Answer</summary>

**A.** Clustering (for example, k-means) is an unsupervised technique that discovers groups of similar data points without predefined labels, which is exactly what customer segmentation without existing categories needs.

Why not the others:
- **B.** Regression predicts a numeric value. It doesn't discover groups.
- **C.** Classification needs categories (and labeled examples) defined in advance. The team doesn't have them yet.
- **D.** Writing descriptions of each customer doesn't group them, and it would be slow and costly at this scale.

Resource: <https://aws.amazon.com/what-is/unsupervised-learning/>
</details>

**22.** A payment processor has millions of past card transactions, each marked "fraud" or "legitimate" after investigation. It wants to score each new transaction as it happens. Which ML problem type is this?
- A. Clustering, because fraud cases can only be found without labels
- B. Regression, because the model must predict the dollar amount of each transaction
- C. Text summarization, because the model must explain each transaction in plain language
- D. Binary classification, because each transaction is predicted as one of two labeled classes

<details><summary>Answer</summary>

**D.** With historical examples labeled as one of two classes, predicting fraud or legitimate for each new transaction is a binary classification problem (supervised learning). The model often outputs a probability that's compared with a threshold.

Why not the others:
- **A.** Unsupervised anomaly detection helps when labels are missing, but this company has labeled outcomes, so supervised classification uses them directly.
- **B.** The transaction amount is already known. The model needs to predict fraud, a category.
- **C.** Summarization produces text. It doesn't decide whether a transaction is fraudulent.

Resource: <https://aws.amazon.com/what-is/supervised-learning/>
</details>

**23.** A call center records thousands of customer calls a day as audio files in Amazon S3. Managers want each call converted to text and then analyzed for customer sentiment, without building or training any models. Which combination of AWS services should they use?
- A. Amazon Polly to convert the audio to text, then Amazon Rekognition to detect sentiment
- B. Amazon Lex to record the calls, then Amazon Textract to read the recordings
- C. Amazon Transcribe to convert speech to text, then Amazon Comprehend to detect sentiment
- D. Amazon Translate to convert the audio to text, then Amazon Personalize to score sentiment

<details><summary>Answer</summary>

**C.** Amazon Transcribe is a managed automatic speech recognition (speech-to-text) service, and Amazon Comprehend is a managed NLP service that detects sentiment, entities, and key phrases in text. Neither requires ML expertise or model training.

```arch
cloud AWS Cloud
  s3: s3 S3 bucket | call recordings
  tr: transcribe *Amazon Transcribe | speech to text
  cm: comprehend *Amazon Comprehend | sentiment
  out: s3 S3 bucket | results
---
1. s3 -> tr : audio
2. tr -> cm : transcript
3. cm -> out : sentiment scores
```

Why not the others:
- **A.** Polly does the opposite (text-to-speech), and Rekognition analyzes images and video, not text sentiment.
- **B.** Lex builds conversational bots, and Textract extracts text from documents and images, not audio.
- **D.** Translate translates text between languages; it doesn't transcribe audio. Personalize generates recommendations, not sentiment.

Resource: <https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html>
</details>

**24.** An e-commerce company wants to show its product descriptions in 12 languages. Its brand names and product line names must never be translated, and the company has no ML staff. Which solution meets these requirements?
- A. Amazon Comprehend with a custom classifier that labels each sentence's language
- B. Amazon Translate with custom terminology that keeps brand and product names unchanged
- C. Amazon Polly with SSML tags that pronounce each product name in 12 languages
- D. A custom translation model trained from scratch on SageMaker AI for each language pair

<details><summary>Answer</summary>

**B.** Amazon Translate is a managed neural machine translation service. Custom terminology lets the company define how specific terms (such as brand names) are translated or left unchanged, without training a model.

Why not the others:
- **A.** Comprehend can detect a text's dominant language, but it doesn't translate text.
- **C.** Polly converts text to speech; it doesn't translate written descriptions.
- **D.** Training translation models from scratch requires large parallel datasets and ML expertise the company doesn't have, and Translate already provides this capability.

Resource: <https://docs.aws.amazon.com/translate/latest/dg/creating-custom-terminology.html>
</details>

**25.** A hotel chain collects 50,000 free-text guest reviews a month. It wants to automatically identify the overall sentiment of each review and extract mentioned entities such as locations, dates, and staff names. Which AWS service should it use?
- A. Amazon Comprehend, which finds sentiment, entities, and key phrases in text
- B. Amazon Rekognition, which detects objects and text in images and videos
- C. Amazon Polly, which turns review text into lifelike speech in many voices
- D. Amazon Personalize, which recommends hotels to guests based on their history

<details><summary>Answer</summary>

**A.** Amazon Comprehend is a managed NLP service that detects sentiment, entities (people, places, dates, organizations), key phrases, language, and PII in text, with no model training required.

Why not the others:
- **B.** Rekognition is computer vision. The reviews are text, not images.
- **C.** Polly synthesizes speech from text; it doesn't analyze meaning or sentiment.
- **D.** Personalize builds recommendation systems. It doesn't analyze review text.

Resource: <https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html>
</details>

**26.** A pizza chain wants a chatbot on its website and phone line that understands requests like "I'd like two large pepperoni pizzas for delivery," asks for any missing details such as the address, and then places the order. Which AWS service is designed for this?
- A. Amazon Textract, which extracts text and form data from scanned documents
- B. Amazon Transcribe, which converts recorded audio files into text transcripts
- C. Amazon Lex, which builds conversational interfaces using intents and slots
- D. Amazon Rekognition, which identifies objects and scenes in images

<details><summary>Answer</summary>

**C.** Amazon Lex builds voice and text chatbots. It recognizes the user's intent (order pizza), collects required details in slots (size, topping, address), prompts for missing values, and can call a Lambda function to fulfill the order.

Why not the others:
- **A.** Textract reads documents; it doesn't hold conversations.
- **B.** Transcribe converts speech to text, but it doesn't understand intents or manage a dialog.
- **D.** Rekognition analyzes images and video, which isn't needed for ordering by chat.

Resource: <https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html>
</details>

**27.** A news website wants every article to be available as audio for visually impaired readers and commuters. It needs natural-sounding voices and control over pronunciation of unusual names. Which AWS service should it use?
- A. Amazon Transcribe, which converts spoken audio into written text
- B. Amazon Comprehend, which extracts key phrases and entities from text
- C. Amazon Lex, which recognizes intents in a customer's spoken requests
- D. Amazon Polly, which converts text to lifelike speech with SSML control

<details><summary>Answer</summary>

**D.** Amazon Polly is a text-to-speech service with many natural-sounding voices. Speech Synthesis Markup Language (SSML) and lexicons give control over pronunciation, pauses, and emphasis.

Why not the others:
- **A.** Transcribe goes the other way: speech to text.
- **B.** Comprehend analyzes text but doesn't produce audio.
- **C.** Lex builds conversational bots; it isn't designed to narrate articles.

Resource: <https://docs.aws.amazon.com/polly/latest/dg/what-is.html>
</details>

**28.** A social media startup lets users upload photos. It must automatically flag images containing explicit or violent content for human review before they are published, and it has no ML team. Which solution should it use?
- A. Amazon Translate to convert any text in the image into a safe language
- B. Amazon Rekognition content moderation to detect unsafe image content
- C. Amazon Textract to extract the image's text and look for banned words
- D. Amazon Comprehend to detect the sentiment of each uploaded photo

<details><summary>Answer</summary>

**B.** Amazon Rekognition's content moderation APIs detect inappropriate, unwanted, or offensive content in images and videos and return labels with confidence scores, so the startup can route suspect uploads to human reviewers.

```arch
users: users App users
cloud AWS Cloud
  s3: s3 S3 bucket | uploads
  fn: lambda Lambda function
  rek: rekognition *Rekognition | content moderation
  q: sqs SQS queue | human review
---
1. users -> s3 : upload photo
2. s3 -> fn : event
3. fn -> rek : DetectModerationLabels
4. fn ~> q : flagged images
```

Why not the others:
- **A.** Translate converts text between languages; it can't judge whether an image is explicit or violent.
- **C.** Textract extracts text, but explicit or violent imagery often contains no text at all.
- **D.** Comprehend analyzes text sentiment, not image content.

Resource: <https://docs.aws.amazon.com/rekognition/latest/dg/moderation.html>
</details>

**29.** A mortgage lender receives thousands of scanned application forms a week. It wants to automatically extract field values (such as applicant name and income) and the contents of tables, keeping the relationship between each label and its value. Which AWS service fits BEST?
- A. Amazon Rekognition, which labels objects, faces, scenes, and text in photos
- B. Amazon Polly, which reads the scanned forms aloud for data entry clerks
- C. Amazon Lex, which interviews each applicant again by chat to collect the values
- D. Amazon Textract, which extracts text, forms, and tables from scanned documents

<details><summary>Answer</summary>

**D.** Amazon Textract goes beyond simple OCR: it extracts text, handwriting, key-value pairs from forms, and table structure from scanned documents, preserving which value belongs to which field.

```arch
cloud AWS Cloud
  s3: s3 S3 bucket | scanned forms
  tx: textract *Amazon Textract | forms and tables
  db: dynamodb DynamoDB | extracted fields
---
1. s3 -> tx : document
2. tx -> db : key-value pairs
```

Why not the others:
- **A.** Rekognition can detect some text in images, but it doesn't understand form fields and table structure in documents.
- **B.** Reading forms aloud would still need people to type the values. It doesn't extract data.
- **C.** Re-interviewing applicants ignores the forms already submitted and adds work.

Resource: <https://docs.aws.amazon.com/textract/latest/dg/what-is.html>
</details>

**30.** A video streaming company wants to show each subscriber a "Recommended for you" row based on viewing history, ratings, and what similar viewers watched. It wants a managed service that doesn't require ML expertise. Which service should it use?
- A. Amazon Personalize, to train a recommender on each subscriber's viewing history
- B. Amazon Comprehend, to detect the sentiment of each movie's plot description
- C. Amazon Rekognition, to identify actors' faces in every movie's trailer
- D. Amazon Transcribe, to generate subtitles for every film in the catalog

<details><summary>Answer</summary>

**A.** Amazon Personalize is a managed service that trains recommendation models on a company's own user, item, and interaction data and serves real-time personalized recommendations, without requiring ML expertise.

```arch
users: users Subscribers
cloud AWS Cloud
  s3: s3 S3 bucket | viewing history
  per: personalize *Amazon Personalize | recommender
  app: app Streaming app
---
1. s3 -> per : interactions
2. app -> per : get recommendations
3. app -> users : recommended row
```

Why not the others:
- **B.** Sentiment of a movie's description doesn't tell the company what each subscriber will want to watch.
- **C.** Recognizing actors in trailers isn't a recommendation engine.
- **D.** Subtitles help accessibility but don't recommend content.

Resource: <https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html>
</details>

**31. (Matching)** A solutions team is mapping business requests to AWS managed AI services. Match each request to the service that handles it.
- Turn recorded doctor dictations into written notes => Amazon Transcribe
- Offer a support website in Japanese, German, and Portuguese => Amazon Translate
- Find the people, organizations, and places mentioned in news articles => Amazon Comprehend
- Give a mobile app a voice that reads notifications aloud => Amazon Polly
- Pull invoice totals and line-item tables out of scanned PDFs => Amazon Textract
- Build a chatbot that books appointments by asking for a date and time => Amazon Lex
Extra choices: Amazon Rekognition | Amazon Personalize

<details><summary>Answer</summary>

Transcribe converts speech to text. Translate translates text between languages. Comprehend performs NLP tasks such as entity recognition and sentiment analysis. Polly converts text to speech. Textract extracts text, forms, and tables from documents. Lex builds conversational bots with intents and slots. Rekognition (images and video) and Personalize (recommendations) don't fit any of these requests.

Resource: <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/machine-learning.html>
</details>

**32. (Ordering)** A company receives customer support calls in Spanish. It wants an English report of each call's sentiment, built only from AWS managed AI services. Select the THREE services the pipeline needs and put them in the order the data passes through them.
- A. Amazon Translate
- B. Amazon Polly
- C. Amazon Transcribe
- D. Amazon Comprehend

<details><summary>Answer</summary>

**C, A, D.** First Amazon Transcribe converts the Spanish audio to Spanish text. Then Amazon Translate translates the transcript to English. Finally Amazon Comprehend detects the sentiment of the English text. (Comprehend also supports Spanish sentiment directly, but the requirement here is an English report, so translation comes before analysis.)

```arch
cloud AWS Cloud
  s3: s3 S3 bucket | Spanish calls
  tr: transcribe Transcribe
  tl: translate Translate
  cm: comprehend Comprehend
---
1. s3 -> tr : audio
2. tr -> tl : Spanish text
3. tl -> cm : English text
```

Why not the others:
- **B.** Amazon Polly converts text to speech. Nothing in this pipeline needs audio output.

Resource: <https://docs.aws.amazon.com/translate/latest/dg/what-is.html>
</details>

**33.** A credit union is choosing an approach for automated loan decisions on structured applicant data. Regulators require the credit union to explain which factors drove each individual decision, and the decisions must be consistent for identical applications. Which approach is MOST appropriate?
- A. A general-purpose LLM prompted with the application, because its free-text answers are easy to read
- B. A traditional ML model trained on the tabular data, with feature-attribution explanations for each decision
- C. An image generation model that visualizes each applicant's financial profile for loan officers
- D. A reinforcement learning agent that experiments with approving different applicants to learn what works

<details><summary>Answer</summary>

**B.** For structured, tabular data with strict explainability and consistency requirements, traditional ML models (such as gradient-boosted trees or logistic regression) are usually a better fit than foundation models. Tools such as SageMaker Clarify can produce per-prediction feature attributions (for example, SHAP values) to explain each decision.

Why not the others:
- **A.** An LLM's explanation is generated text, not a faithful account of how it reached the decision, and its outputs can vary between runs, which conflicts with the consistency and explainability rules.
- **C.** Images of profiles don't make decisions or explain them.
- **D.** Experimenting with real loan approvals is risky and wouldn't satisfy regulators' explainability requirements.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-explainability.html>
</details>

**34.** A law firm wants to produce short summaries of thousands of contracts, emails, and memos that vary widely in format. It has no labeled examples of "good summaries" and wants results within weeks. Which approach is MOST appropriate?
- A. Collect and label 100,000 summaries, then train a custom model from scratch
- B. Use a clustering algorithm to group documents and print the cluster names as summaries
- C. Use a pre-trained foundation model through a managed service, guided by well-designed prompts
- D. Build a regression model that predicts the ideal word count of each document's summary

<details><summary>Answer</summary>

**C.** Foundation models are pre-trained on broad data and can summarize varied unstructured documents with zero-shot or few-shot prompting, so no labeled dataset or training is needed. Using one through a managed service such as Amazon Bedrock gets results quickly.

Why not the others:
- **A.** Labeling and training from scratch would take months and cost far more, for a capability FMs already provide.
- **B.** Cluster names describe groups of documents, not the contents of each document.
- **D.** Predicting a word count doesn't produce a summary.

Resource: <https://aws.amazon.com/what-is/foundation-models/>
</details>

**35.** A manufacturing company is deciding where AI could add the most value. Which TWO opportunities are good fits for AI/ML? (Select TWO.)
- A. Inspecting 20,000 parts per hour on a production line for visual defects that human inspectors often miss
- B. Calculating the total of each invoice by adding up its line items, which must always be exact
- C. Recording the date that each new employee started, as entered by the HR team
- D. Forecasting demand for spare parts across 300 warehouses using years of usage history
- E. Sorting a list of supplier names into alphabetical order for a printed directory

<details><summary>Answer</summary>

**A, D.** AI/ML adds value when tasks need pattern recognition at a scale or speed people can't match (visual inspection of every part) or when predictions improve decisions using lots of historical data (demand forecasting across many locations).

Why not the others:
- **B.** Summing line items is an exact arithmetic task that ordinary code does perfectly. A prediction adds nothing.
- **C.** Recording a date someone entered is data entry, not a pattern-recognition or prediction problem.
- **E.** Alphabetical sorting is a deterministic algorithm. ML isn't needed.

Resource: <https://aws.amazon.com/ai/machine-learning/>
</details>

## Task 1.3: Describe the AI/ML development lifecycle

**36. (Ordering)** A team is planning its first custom ML project to predict customer churn. Put these stages of the ML development lifecycle in order, from first to last.
- A. Train the model on the prepared data
- B. Deploy the model and monitor it in production
- C. Collect data and define the business goal
- D. Evaluate the model against a held-out test set
- E. Clean the data and engineer features

<details><summary>Answer</summary>

**C, E, A, D, B.** An ML project starts by defining the business problem and collecting data, then preparing it (cleaning, exploratory analysis, feature engineering), training the model, evaluating it on data it hasn't seen, and finally deploying it and monitoring it so it can be retrained when performance drifts.

```arch
row [row]
  c: s3 Collect data
  e: databrew Prepare data
  a: train *Train
  d: model Evaluate
  b: sagemaker Deploy and monitor
---
c -> e
e -> a
a -> d
d -> b
b ~> c : retrain on new data
```

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html>
</details>

**37.** A startup wants a model that answers customer questions about gardening. It is considering pre-training its own foundation model from scratch versus starting from an existing open-source pre-trained model. What is the MAIN advantage of starting from a pre-trained model?
- A. Pre-trained models never need any evaluation or testing before use in production
- B. Pre-trained models are guaranteed to be free of bias because they were trained by experts
- C. It avoids the enormous data, compute, and expertise that pre-training from scratch requires
- D. A pre-trained model can only be used for the exact task it was originally trained on

<details><summary>Answer</summary>

**C.** Pre-training a foundation model requires massive datasets, large GPU clusters for weeks or months, and specialized expertise. Starting from an existing pre-trained model (for example, from Amazon SageMaker JumpStart or Amazon Bedrock) and then prompting, using RAG, or fine-tuning it is far cheaper and faster.

Why not the others:
- **A.** Every model should be evaluated for accuracy, safety, and fit before production, whatever its source.
- **B.** Pre-trained models can carry biases from their training data. They aren't guaranteed to be bias-free.
- **D.** Pre-trained foundation models are general-purpose and can be adapted to many tasks; that's their key benefit.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-foundation-models.html>
</details>

**38.** A five-person software company wants to add a text-summarization feature using a foundation model. It doesn't want to manage servers, GPUs, or model hosting, and it wants to pay only for what it uses. Which way of using the model in production fits BEST?
- A. Call the model through a managed API service such as Amazon Bedrock with on-demand pricing
- B. Download the model weights and host them on a fleet of self-managed Amazon EC2 GPU instances
- C. Train a new model on SageMaker AI and deploy it to a dedicated real-time endpoint
- D. Run the model on employees' laptops and sync the summaries to Amazon S3 each night

<details><summary>Answer</summary>

**A.** A managed API service such as Amazon Bedrock gives access to foundation models through a single API with no infrastructure to manage. With on-demand pricing, the company pays per token processed.

```arch
users: users Customers
cloud AWS Cloud
  app: lambda App backend | Lambda
  br: bedrock *Amazon Bedrock | managed FM API
---
1. users -> app : summarize request
2. app -> br : InvokeModel
3. br -> app : summary
```

Why not the others:
- **B.** Self-hosting on EC2 means managing GPUs, scaling, patching, and model serving, which the company wants to avoid.
- **C.** Training a new model is unnecessary for summarization, and a dedicated endpoint is billed while it runs, whether or not it is used.
- **D.** Laptops aren't a reliable or scalable production environment and add delay.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>
</details>

**39.** A research lab has fine-tuned an open-source model with its own proprietary weights. It needs full control over the serving container, the instance type, and how the model scales, while still avoiding managing physical servers. Which option fits BEST?
- A. Use Amazon Comprehend's built-in entity recognition, which hosts any model the lab uploads
- B. Use Amazon Polly to serve the model because Polly supports custom neural network weights
- C. Paste the model weights into a prompt for a foundation model in the Amazon Bedrock playground
- D. Deploy the model to an Amazon SageMaker AI endpoint, choosing the instance type and container

<details><summary>Answer</summary>

**D.** A SageMaker AI endpoint is a self-hosted (but managed-infrastructure) option: the lab picks the instance type, container, and scaling policy and deploys its own model artifacts, while AWS manages the underlying hardware.

Why not the others:
- **A.** Comprehend provides its own NLP models and supports custom classifiers and entity recognizers it trains itself. It doesn't host arbitrary models.
- **B.** Polly is a text-to-speech service with AWS-provided voices. It doesn't serve customer models.
- **C.** Model weights can't be loaded by pasting them into a prompt. A prompt is input text for a model, not a way to deploy one.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html>
</details>

**40. (Matching)** A team is choosing Amazon SageMaker AI features for each stage of its ML pipeline. Match each need to the feature that serves it.
- Have human workers label thousands of images to create training data => SageMaker Ground Truth
- Explore, clean, and transform data with a visual interface before training => SageMaker Data Wrangler
- Store curated features so training and inference use the same values => SageMaker Feature Store
- Detect when production data or prediction quality drifts from the baseline => SageMaker Model Monitor
- Keep versions of approved models and track which is deployed => SageMaker Model Registry
- Automate the repeatable steps from data processing to deployment => SageMaker Pipelines

<details><summary>Answer</summary>

Ground Truth manages data labeling. Data Wrangler prepares data visually. Feature Store stores and serves features consistently for training and inference. Model Monitor watches deployed models for data and quality drift. Model Registry catalogs model versions and their approval status. Pipelines automates ML workflows so they're repeatable.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html>
</details>

**41.** A sales operations manager with no ML or coding skills wants to ask questions in plain English about the company's sales data, get dashboards and cited answers that draw on internal documents, and automate routine follow-up tasks. Which AWS service is designed for this kind of business user?
- A. Amazon SageMaker AI, which requires building and training custom models in notebooks
- B. Amazon Quick, which offers AI agents, research, automation, and BI by chat
- C. Amazon EMR, which runs big data frameworks such as Apache Spark on managed clusters
- D. AWS Glue, which crawls data sources and runs ETL jobs written by data engineers

<details><summary>Answer</summary>

**B.** Amazon Quick (which evolved from Amazon QuickSight) is a fully managed, AI-powered workspace for business users. Its features include Quick Sight dashboards, Quick Research for cited reports, Quick Flows and Quick Automate for automation, and Quick Index to ground answers in company documents, all used through natural-language chat.

Why not the others:
- **A.** SageMaker AI is for data scientists and ML engineers who build, train, and deploy models.
- **C.** EMR runs big data processing clusters, which need engineering skills to use.
- **D.** Glue is a data integration service for engineers building ETL pipelines, not a natural-language analytics tool.

Resource: <https://docs.aws.amazon.com/quick/latest/userguide/what-is.html>
</details>

**42.** A development team wants an AI-powered development environment that turns a feature request into written requirements, a design, and a task list before generating code, and that applies the team's coding standards automatically. Which AWS offering is built for this spec-driven approach?
- A. Amazon Polly, which reads requirements documents aloud to developers
- B. AWS Artifact, which provides AWS compliance reports for download
- C. Amazon Personalize, which recommends code snippets based on past commits
- D. Kiro, an agentic IDE that uses specs, steering files, and agent hooks

<details><summary>Answer</summary>

**D.** Kiro is an AI-powered development environment. Its specs turn a request into requirements, a design, and implementation tasks; steering files encode project standards; and agent hooks trigger actions automatically when files change or tasks complete. It can also connect to external tools through MCP.

Why not the others:
- **A.** Polly is text-to-speech. It doesn't plan or write software.
- **B.** AWS Artifact is a portal for compliance reports and agreements, unrelated to software development.
- **C.** Personalize builds recommendation systems for users and items. It isn't a development tool.

Resource: <https://kiro.dev/docs/specs/>
</details>

**43.** A retailer's demand-forecasting model was accurate at launch, but six months later its predictions are getting worse because shopping patterns changed. The ML team wants to detect this automatically and retrain the model with recent data without manual steps. Which approach reflects MLOps best practice?
- A. Wait for store managers to complain, then retrain the model by hand on a data scientist's laptop
- B. Use SageMaker Model Monitor to detect drift and trigger a SageMaker Pipelines retraining workflow
- C. Freeze the model forever, because changing a production model always increases technical debt
- D. Replace the model with a larger foundation model, because large models never drift

<details><summary>Answer</summary>

**B.** MLOps applies automation and monitoring to the ML lifecycle. Model Monitor compares production data and predictions with a baseline and raises alerts (through CloudWatch) when they drift, and a SageMaker Pipelines workflow can retrain, evaluate, and register a new model version in a repeatable way.

```arch
cloud AWS Cloud
  ep: sagemaker Production endpoint
  mon: sagemaker *Model Monitor | drift detection
  cw: cloudwatch CloudWatch alarm
  pipe: sagemaker *SageMaker Pipelines | retrain, evaluate
  reg: model Model Registry
---
1. ep -> mon : captured data
2. mon -> cw : drift metrics
3. cw -> pipe : trigger retraining
4. pipe -> reg : new version
5. reg ~> ep : approved deploy
```

Why not the others:
- **A.** Manual, ad hoc retraining isn't repeatable or scalable, and relying on complaints means problems are found late.
- **C.** Models degrade when data changes. Monitoring and retraining are core to keeping them useful.
- **D.** Any model can degrade when real-world data shifts, and a bigger model wouldn't solve a changed-data problem.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html>
</details>

**44.** A company's ML team keeps losing track of which dataset and settings produced each model, and every deployment involves dozens of manual steps. Which TWO MLOps practices address these problems? (Select TWO.)
- A. Track experiments, data versions, and parameters so each model can be reproduced
- B. Let each data scientist deploy models in their own way to encourage creativity
- C. Delete old datasets after training to save storage and reduce clutter
- D. Automate the training-to-deployment workflow so it runs the same way every time
- E. Skip evaluation for small model updates to speed up the release process

<details><summary>Answer</summary>

**A, D.** MLOps emphasizes experimentation tracking and versioning (so any model can be traced back to its data, code, and parameters) and repeatable, automated processes (so deployment is consistent and scalable). On AWS, SageMaker AI experiment tracking, Model Registry, and Pipelines support these practices.

Why not the others:
- **B.** Inconsistent, individual deployment processes create the very technical debt and errors MLOps aims to remove.
- **C.** Deleting training data makes models impossible to reproduce or audit.
- **E.** Skipping evaluation risks shipping worse models. Automated evaluation gates are part of production readiness.

Resource: <https://aws.amazon.com/what-is/mlops/>
</details>

**45.** A hospital builds a model that screens scans for a serious but treatable disease. Missing a sick patient is far worse than flagging a healthy patient for a follow-up test. Which metric should the team prioritize?
- A. Precision, because it measures how many flagged patients are actually sick
- B. Training time, because faster training lets the hospital retrain more often
- C. Recall, because it measures how many sick patients the model catches
- D. Accuracy alone, because it always reflects the cost of each type of mistake

<details><summary>Answer</summary>

**C.** Recall (sensitivity) = true positives ÷ (true positives + false negatives). Prioritizing recall minimizes false negatives, which are missed sick patients, at the cost of some extra false positives that a follow-up test can resolve.

Why not the others:
- **A.** Precision measures how many positive predictions are correct. Optimizing it reduces false alarms but can miss sick patients.
- **B.** Training time affects cost and agility, not how well the model catches the disease.
- **D.** Accuracy treats all errors equally and can look high even when the model misses many rare positive cases.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality.html>
</details>

**46.** An email provider's spam filter moves suspected spam out of the inbox. Users are very unhappy when a real email from their bank or employer is wrongly moved, but they tolerate seeing an occasional spam message. Which metric matters MOST?
- A. Precision, because it measures how many emails flagged as spam really are spam
- B. Recall, because catching every spam message matters more than any other goal
- C. Mean absolute error, because it measures how far each prediction is from the true value
- D. ROUGE, because it measures how well the filter summarizes each email

<details><summary>Answer</summary>

**A.** Precision = true positives ÷ (true positives + false positives). High precision means few legitimate emails (false positives) are flagged as spam, which is what users care about most here.

Why not the others:
- **B.** Maximizing recall would catch more spam but usually increases false positives, moving more real emails.
- **C.** Mean absolute error is a regression metric for numeric predictions, not for a spam/not-spam classifier.
- **D.** ROUGE evaluates generated summaries against reference text. It doesn't apply to classification.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality.html>
</details>

**47.** A fraud model is evaluated on a dataset in which only 0.5% of transactions are fraudulent. A model that labels every transaction as "legitimate" scores 99.5% accuracy. Which metric gives a more meaningful single view of the model's performance on the fraud class?
- A. Accuracy on the training set instead of the test set
- B. F1 score, the harmonic mean of precision and recall
- C. The number of rows in the evaluation dataset
- D. The model's inference latency in milliseconds

<details><summary>Answer</summary>

**B.** With imbalanced classes, accuracy is misleading because always predicting the majority class scores well. The F1 score combines precision and recall for the positive (fraud) class into one number, so a model that never catches fraud gets an F1 of 0.

Why not the others:
- **A.** Training-set accuracy is even less informative: it hides overfitting and has the same imbalance problem.
- **C.** Dataset size isn't a performance metric.
- **D.** Latency measures speed, not how well the model detects fraud.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality.html>
</details>

**48.** Leadership asks whether a new product-recommendation model is worth what it cost. Which TWO metrics are business metrics rather than model performance metrics? (Select TWO.)
- A. Return on investment (ROI) from the extra revenue the recommendations generate
- B. The model's precision on a held-out test set of past purchases
- C. Cost per user of running the recommendation service each month
- D. The model's recall for items customers eventually bought
- E. The F1 score measured during the last training run

<details><summary>Answer</summary>

**A, C.** Business metrics measure the value and cost of an ML solution to the organization: ROI, cost per user, development costs, customer feedback, and similar. Precision, recall, and F1 are model performance metrics that describe how well the model predicts.

Why not the others:
- **B.** Precision is a model performance metric.
- **D.** Recall is a model performance metric.
- **E.** F1 is a model performance metric.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html>
</details>

**49.** A team needs to put foundation models to work in several ways: a public chat app with no servers to manage, a data scientist's experiment that fine-tunes an open-source model from a curated catalog, and business analysts who want natural-language answers over company data. Which pairing of needs to AWS services is correct?
- A. Chat app: Amazon Bedrock; fine-tuning: SageMaker JumpStart; analysts: Amazon Quick
- B. Chat app: Amazon Polly; fine-tuning: Amazon Lex; analysts: Amazon Textract
- C. Chat app: Amazon EC2 only; fine-tuning: AWS Artifact; analysts: Amazon Rekognition
- D. Chat app: SageMaker Ground Truth; fine-tuning: Amazon Personalize; analysts: AWS Glue

<details><summary>Answer</summary>

**A.** Amazon Bedrock provides serverless API access to foundation models for applications. SageMaker JumpStart is a hub of pre-trained (including open-source) models that data scientists can deploy and fine-tune in SageMaker AI. Amazon Quick gives business users natural-language analytics, research, and agents over their data.

Why not the others:
- **B.** Polly is text-to-speech, Lex builds chatbots but doesn't fine-tune models, and Textract extracts document data rather than answering analysts' questions.
- **C.** EC2 means managing servers, AWS Artifact provides compliance reports, and Rekognition analyzes images.
- **D.** Ground Truth labels data, Personalize builds recommenders, and Glue runs ETL; none fits the stated need.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html>
</details>

**50.** An ML team has a model that performs well in a notebook. Before it serves real customers, the team lead asks what "production readiness" requires. Which answer reflects MLOps practice BEST?
- A. Production readiness means the model scored well once, so it can be copied straight to production
- B. It means retraining the model by hand every day, whether or not its performance has changed
- C. It means choosing the largest available instance type so the model never needs monitoring
- D. It means automated evaluation, versioned artifacts, scalable serving, and monitoring with retraining

<details><summary>Answer</summary>

**D.** Production readiness covers more than accuracy in a notebook: repeatable automated evaluation, versioned code, data, and models, infrastructure that scales with demand, and monitoring that detects drift and triggers retraining. These reduce technical debt and keep the model reliable after launch.

Why not the others:
- **A.** A single good notebook result doesn't show that the model is reproducible, scalable, or monitored.
- **B.** Manual daily retraining is costly and error-prone. Retraining should be driven by monitoring and automated.
- **C.** Bigger instances help capacity, but performance can still degrade as data changes, so monitoring is always needed.

Resource: <https://aws.amazon.com/what-is/mlops/>
</details>
