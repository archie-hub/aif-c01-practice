# Domain 4: Guidelines for Responsible AI (14%)

Guide page: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain4.html>

---

## Task 4.1: Explain the development of AI systems that are responsible

**1.** A hiring platform uses a model to rank job applicants. An audit shows that, with equal qualifications, applicants from one age group are ranked lower than others. Which responsible AI feature is the model failing?
- A. Robustness, because the model crashes on unusual inputs
- B. Veracity, because the model writes inaccurate text
- C. Latency, because rankings take too long to compute
- D. Fairness, because outcomes differ unjustly across groups

<details><summary>Answer</summary>

**D.** Fairness means a system's outcomes don't unjustly favor or disadvantage individuals or groups, for example by age, gender, or ethnicity. Systematically lower rankings for equally qualified people in one age group is a fairness failure, often caused by bias in the training data.

Why not the others:
- **A.** Robustness concerns reliable behavior under unexpected or adversarial inputs. Nothing is crashing here.
- **B.** Veracity concerns truthful, accurate outputs. The problem is unequal treatment of groups.
- **C.** Latency is speed, not a responsible AI feature.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**2.** A government agency builds a voice assistant for public services. Testing shows it works well for native speakers but often misunderstands people with regional accents, older adults, and speech impairments. Which responsible AI feature should the agency improve?
- A. Prompt caching, so repeated questions are answered faster
- B. Model distillation, so the model is smaller and cheaper
- C. Inclusivity, so the system works well for everyone who uses it
- D. Token efficiency, so the assistant uses fewer tokens per reply

<details><summary>Answer</summary>

**C.** Inclusivity means designing and testing AI systems so they serve diverse users, including different accents, ages, abilities, and languages. That usually requires more diverse training and test data and testing with representative user groups.

Why not the others:
- **A.** Caching improves speed and cost, not who the system works for.
- **B.** A smaller model doesn't address groups the system fails to understand.
- **D.** Token efficiency is a cost concern, not an inclusivity one.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**3.** An image classifier for detecting road signs works in clear weather but fails when signs are partly covered by snow or slightly altered with stickers. Which responsible AI feature is weak?
- A. Robustness
- B. Transparency
- C. Inclusivity
- D. Explainability

<details><summary>Answer</summary>

**A.** Robustness is the ability to keep performing reliably when inputs are noisy, unusual, or deliberately manipulated. Testing with varied and adversarial inputs and training on more varied data improve it.

Why not the others:
- **B.** Transparency is about openness on how the system works and is used.
- **C.** Inclusivity concerns serving diverse groups of people.
- **D.** Explainability is about understanding why a model made a prediction.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**4.** A children's homework helper must never produce violent, sexual, or otherwise harmful content, even if a child asks for it. Which responsible AI feature does this requirement address MOST directly?
- A. Cost efficiency
- B. Safety
- C. Multilingual support
- D. Throughput

<details><summary>Answer</summary>

**B.** Safety means preventing harmful outputs and misuse, protecting users (especially vulnerable ones such as children) from harmful content. On AWS, Bedrock Guardrails content filters and denied topics help enforce safety.

Why not the others:
- **A.** Cost efficiency is a business goal, not a protection against harm.
- **C.** Language support doesn't prevent harmful content.
- **D.** Throughput is capacity, not safety.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html>
</details>

**5.** A financial news assistant sometimes states incorrect stock figures with total confidence. Which responsible AI feature is most concerned with outputs being truthful and correct?
- A. Controllability
- B. Inclusivity
- C. Portability
- D. Veracity

<details><summary>Answer</summary>

**D.** Veracity (often paired with robustness) is about AI outputs being correct and truthful. Grounding answers in authoritative data, contextual grounding checks, and human review improve veracity.

Why not the others:
- **A.** Controllability is about being able to monitor and steer AI behavior.
- **B.** Inclusivity concerns serving diverse users.
- **C.** Portability isn't one of the responsible AI dimensions.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**6. (Matching)** An AI ethics board is mapping its policies to AWS's dimensions of responsible AI. Match each policy statement to the dimension it supports.
- Loan decisions must not disadvantage applicants based on gender or ethnicity => Fairness
- Customers can learn which factors led to a decision about them => Explainability
- Customer data used by AI is protected and used only as permitted => Privacy and security
- The system must avoid producing harmful content or enabling misuse => Safety
- Operators can monitor and correct the system's behavior when needed => Controllability
- Stakeholders are told when and how AI is used so they can make informed choices => Transparency

<details><summary>Answer</summary>

AWS describes responsible AI dimensions that include fairness, explainability, privacy and security, safety, controllability, veracity and robustness, governance, and transparency. Each policy maps to the dimension whose goal it serves.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**7.** A community forum adds a generative AI assistant. The team wants to block hate speech, insults, and sexual or violent content in both user prompts and model responses, with adjustable strength per category. Which feature should it configure?
- A. Prompt caching for Amazon Bedrock models
- B. Amazon Bedrock Guardrails content filters
- C. Amazon Macie sensitive data discovery
- D. AWS Budgets alerts for the forum's account

<details><summary>Answer</summary>

**B.** Guardrails content filters detect and filter harmful content in categories such as hate, insults, sexual, violence, and misconduct, with configurable filter strength for inputs and outputs.

Why not the others:
- **A.** Prompt caching reduces cost and latency.
- **C.** Macie finds sensitive data in Amazon S3. It doesn't moderate conversations.
- **D.** Budgets tracks spending.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html>
</details>

**8.** A RAG assistant for an insurance company occasionally adds coverage details that aren't in the retrieved policy documents. The team wants to automatically detect and block responses that aren't supported by the source passages. Which Bedrock Guardrails feature fits?
- A. Word filters
- B. Denied topics
- C. Contextual grounding checks
- D. Content filters for insults

<details><summary>Answer</summary>

**C.** Contextual grounding checks score whether a response is grounded in the provided source information and relevant to the user's query, and can block or flag responses below a threshold. That helps catch hallucinations in RAG applications.

```arch
row
  kb: bedrock Knowledge Base | retrieved passages
  fm: bedrock Foundation model
  gr: bedrock *Guardrail | contextual grounding check
  user: users Customer
---
kb -> fm : context
fm -> gr : draft answer
gr -> user : grounded answers only
```

Why not the others:
- **A.** Word filters block exact words or phrases. They can't judge whether an answer is supported.
- **B.** Denied topics block whole subject areas, not unsupported details.
- **D.** Insult filters target abusive language, not accuracy.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html>
</details>

**9.** An HR chatbot answers questions about leave eligibility, which follows precise rules (for example, length of service and employment type). The company wants to mathematically verify that the chatbot's answers comply with those rules. Which Bedrock Guardrails capability is designed for this?
- A. Automated Reasoning checks, which validate answers against logical rules
- B. Content filters, which score responses for hate, insults, and violence
- C. Word filters, which block profanity and custom phrases
- D. Prompt attack filters, which detect jailbreak attempts

<details><summary>Answer</summary>

**A.** Automated Reasoning checks use formal logic to validate whether model responses are consistent with rules and policies the company defines (written in natural language and translated into logic), flagging answers that contradict them.

```arch
row
  fm: bedrock HR chatbot | foundation model
  ar: bedrock *Automated Reasoning check
  pol: document Leave policy | logical rules
  emp: user Employee
---
fm -> ar : proposed answer
pol -> ar : rules
ar -> emp : validated answer
```

Why not the others:
- **B.** Content filters detect harmful content, not rule compliance.
- **C.** Word filters match specific words.
- **D.** Prompt attack filters protect against manipulation of the prompt, not policy accuracy.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html>
</details>

**10.** A retailer's assistant must never mention specific competitor brand names in its responses. Which Bedrock Guardrails feature handles this MOST simply?
- A. Contextual grounding checks on each response
- B. Sensitive information filters for personal data
- C. Word filters with a list of competitor names
- D. Automated Reasoning checks against a policy

<details><summary>Answer</summary>

**C.** Word filters block exact custom words and phrases (as well as profanity) in inputs and outputs, which suits a fixed list of competitor names.

Why not the others:
- **A.** Grounding checks evaluate whether answers are supported by sources.
- **B.** PII filters detect personal data such as names and phone numbers of people, not brand names.
- **D.** Automated Reasoning validates answers against logical rules, which is unnecessary for a simple blocklist.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html>
</details>

**11.** An education company is building a tutoring assistant for students aged 10–14. It must refuse to discuss gambling and must not reveal students' phone numbers or email addresses. Which TWO Bedrock Guardrails policies should it configure? (Select TWO.)
- A. A denied topic that describes gambling
- B. Model distillation from a larger model
- C. A sensitive information filter that blocks or masks phone numbers and email addresses
- D. Provisioned Throughput for the tutoring model
- E. A prompt template with a variable for the student's name

<details><summary>Answer</summary>

**A, C.** Denied topics block conversations on defined subjects such as gambling. Sensitive information filters detect PII types such as phone numbers and email addresses and block or mask them.

Why not the others:
- **B.** Distillation creates a smaller model; it isn't a safety policy.
- **D.** Provisioned Throughput reserves capacity.
- **E.** Prompt templates structure prompts but don't enforce restrictions.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html>
</details>

**12.** A company with sustainability commitments is choosing a model for a simple text-classification feature. Two models meet the accuracy requirement: a very large model and a much smaller one. Which choice reflects responsible model selection?
- A. The larger model, because more parameters always signal more responsible AI
- B. Whichever model was released most recently, regardless of size
- C. Both models running in parallel for every request to compare answers
- D. The smaller model, because it needs less compute and energy for the same outcome

<details><summary>Answer</summary>

**D.** Environmental impact is part of responsible model selection. When a smaller model meets requirements, it uses less compute and energy per request, which lowers both carbon footprint and cost.

Why not the others:
- **A.** Size isn't a measure of responsibility, and extra compute increases energy use.
- **B.** Release date says nothing about efficiency or fit.
- **C.** Running both doubles compute and energy for no benefit.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html>
</details>

**13.** A team wants to reduce the environmental footprint of its ML workloads on AWS. Which TWO practices help? (Select TWO.)
- A. Retrain every model daily even when its performance hasn't changed
- B. Use purpose-built, energy-efficient accelerators such as AWS Trainium and AWS Inferentia where suitable
- C. Keep development GPU instances running all weekend in case they're needed
- D. Reuse pre-trained models and fine-tune them instead of training large models from scratch
- E. Store multiple duplicate copies of every training dataset in different buckets

<details><summary>Answer</summary>

**B, D.** Efficient hardware and avoiding unnecessary training (by reusing and fine-tuning pre-trained models) reduce energy use. The AWS Well-Architected sustainability guidance for ML also recommends retraining only when needed and removing idle resources.

Why not the others:
- **A.** Unneeded retraining wastes compute and energy.
- **C.** Idle instances consume energy and money without benefit.
- **E.** Unnecessary duplicate data increases storage footprint.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html>
</details>

**14.** A marketing agency uses an image generation model to create ad artwork. A client points out that one generated image closely resembles a famous copyrighted illustration. Which legal risk of generative AI does this illustrate?
- A. Intellectual property infringement
- B. Model drift in production data
- C. Data residency regulation violation
- D. Underfitting of the image model

<details><summary>Answer</summary>

**A.** Generative models can produce content that closely resembles copyrighted or trademarked works from their training data, which can lead to IP infringement claims. Reviewing outputs, choosing models and providers with IP protections, and documenting usage reduce the risk.

Why not the others:
- **B.** Drift is degraded performance over time, not a legal claim about content.
- **C.** Residency concerns where data is stored or processed.
- **D.** Underfitting is a training problem.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**15.** An airline's chatbot invents a refund policy that doesn't exist and promises a customer a refund. The customer later demands the refund. Which risks does this illustrate?
- A. Lower token costs and faster responses for customers
- B. End-user harm and loss of trust from hallucinated output
- C. Improved explainability of the model's internal reasoning
- D. Better inclusivity for international travelers

<details><summary>Answer</summary>

**B.** Hallucinated answers can mislead users, create legal and financial exposure for the business, and damage customer trust. Grounding, guardrails, and clear disclaimers or human escalation for commitments reduce this risk.

Why not the others:
- **A.** The incident isn't about cost or speed.
- **C.** An invented policy reveals nothing about how the model reasons.
- **D.** Inclusivity isn't the issue in this scenario.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html>
</details>

**16.** A publisher plans to release AI-generated articles without human review. Which TWO legal or business risks should it consider? (Select TWO.)
- A. Biased statements about groups of people, leading to legal action
- B. Lower storage costs for the published articles in Amazon S3
- C. Articles that reproduce copyrighted text from other publications
- D. Faster page loads for readers on mobile devices
- E. Fewer AWS Regions needed to serve the website globally

<details><summary>Answer</summary>

**A, C.** Biased output and IP infringement are key legal risks of generative AI. Both can lead to legal claims and reputational damage, which human review and guardrails help prevent.

Why not the others:
- **B.** Storage cost isn't a legal risk.
- **D.** Page speed is a performance benefit.
- **E.** Regional footprint is an infrastructure decision, not a legal risk.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**17.** A team is building a model to detect a rare equipment fault. Its training data has 99,000 "normal" examples and only 1,000 "fault" examples, and the model rarely predicts faults. Which dataset characteristic should the team address?
- A. Class balance, by collecting more fault examples or resampling
- B. The number of columns, by deleting most features
- C. The file format, by converting all CSV training files to JSON
- D. The storage class of the data, by moving it to S3 Glacier

<details><summary>Answer</summary>

**A.** Imbalanced datasets lead models to favor the majority class. Balancing (collecting more minority examples, oversampling, undersampling, or weighting) helps the model learn the rare class. Tools such as SageMaker Clarify can measure class imbalance before training.

Why not the others:
- **B.** Removing features doesn't fix the imbalance and may remove useful signals.
- **C.** File format has no effect on class balance.
- **D.** Storage class doesn't change the data's content.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-data-bias.html>
</details>

**18.** A health information app plans to fine-tune a model. The team can use either random health forum posts scraped from the internet or articles reviewed by medical professionals from licensed sources. Which choice reflects responsible dataset practice?
- A. The forum posts, because more informal data always produces a friendlier model
- B. A random mix of both without checking either source
- C. The curated, licensed, professionally reviewed articles
- D. Neither, because fine-tuning should never use any data

<details><summary>Answer</summary>

**C.** Curated data sources with known quality, accuracy, and licensing reduce the risk of the model learning misinformation, bias, or content the company has no right to use.

Why not the others:
- **A.** Unvetted posts can contain misinformation and unknown licensing terms.
- **B.** Mixing in unchecked data still brings in its risks.
- **D.** Fine-tuning requires data. The question is which data to use.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-prepare.html>
</details>

**19.** A speech-to-text startup trains its model mostly on recordings from young adults in one country. It plans to sell to call centers around the world. What should it do to build a more inclusive model?
- A. Only market the product to one country and age group forever
- B. Collect diverse training data covering many accents and ages
- C. Increase the model's temperature to handle unfamiliar accents
- D. Reduce the training data so the model generalizes better

<details><summary>Answer</summary>

**B.** Diverse, representative training data is the foundation of inclusive AI. A model can't reliably serve groups that are missing from its data.

Why not the others:
- **A.** Restricting the market avoids the problem rather than building an inclusive product.
- **C.** Temperature applies to generative sampling, not to recognizing accents.
- **D.** Removing data doesn't add the missing diversity.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**20.** A face-detection model performs with 98% accuracy overall but only 85% accuracy for people with darker skin tones. What is the MOST likely cause, and what is the effect?
- A. The model has too many parameters, which lowers accuracy for everyone equally
- B. The model's latency is too high, which lowers accuracy for some groups of users
- C. The test images were encrypted, which reduced accuracy for some of the photos
- D. Groups under-represented in the training data get biased, less accurate results

<details><summary>Answer</summary>

**D.** When some demographic groups are under-represented in training data, models tend to perform worse for them. That's bias with real effects on those groups, which can be hidden in an overall accuracy figure. Measuring performance by subgroup reveals it.

Why not the others:
- **A.** Parameter count doesn't explain a gap that affects one group specifically.
- **B.** Latency doesn't change prediction accuracy.
- **C.** Encryption is removed before data is used, so it doesn't affect accuracy.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-data-bias.html>
</details>

**21.** A credit model's predictions change a lot when it's retrained on slightly different samples of the same data, and it performs much worse on new applicants than on training data. Which problem does this describe, and what is a likely consequence?
- A. High bias (underfitting), leading to identical decisions for every applicant
- B. Low variance, meaning the model is perfectly stable and needs no changes
- C. High variance (overfitting), giving unreliable and possibly unfair decisions
- D. Data residency issues, because the model was trained in another Region

<details><summary>Answer</summary>

**C.** High variance means a model is too sensitive to the specific training data (overfitting). It generalizes poorly, so decisions for new people are inaccurate and inconsistent, which can also produce unfair outcomes for some groups.

Why not the others:
- **A.** High bias (underfitting) gives poor performance even on training data and doesn't make predictions swing between retraining runs.
- **B.** The large performance gap and sensitivity show high variance, not stability.
- **D.** The Region used for training doesn't explain unstable predictions.

Resource: <https://aws.amazon.com/what-is/overfitting/>
</details>

**22.** Before training a loan-approval model, a bank wants to measure whether its training data is imbalanced across age groups and genders. After training, it wants to check whether predictions differ unfairly between those groups. Which AWS tool supports both checks?
- A. Amazon SageMaker Clarify
- B. Amazon Polly with SSML
- C. AWS Cost Explorer reports
- D. Amazon CloudFront logs

<details><summary>Answer</summary>

**A.** SageMaker Clarify computes pre-training bias metrics on datasets (such as class imbalance across a facet like age or gender) and post-training bias metrics on model predictions. It also provides explainability through feature attributions.

```arch
cloud AWS Cloud
  s3: s3 Training data
  clar1: sagemaker *Clarify | pre-training bias
  train: train Training job
  clar2: sagemaker *Clarify | post-training bias
  rep: document Bias report
---
1. s3 -> clar1
2. clar1 -> train : data accepted
3. train -> clar2 : model
4. clar2 -> rep
```

Why not the others:
- **B.** Polly is a text-to-speech service.
- **C.** Cost Explorer analyzes spending.
- **D.** CloudFront delivers web content.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-configure-processing-jobs.html>
</details>

**23.** A company's model sometimes makes low-confidence predictions on medical claims. It wants those predictions routed to human reviewers, with the reviews used to audit the model's trustworthiness over time. Which AWS service is designed to add this human review step?
- A. Amazon Comprehend custom classification
- B. Amazon Augmented AI (A2I)
- C. AWS Glue workflows
- D. Amazon S3 Glacier archives

<details><summary>Answer</summary>

**B.** Amazon A2I builds human review workflows for ML predictions. Rules (such as confidence below a threshold) send predictions to human reviewers, and the reviews support audits and further training.

```arch
row
  model: sagemaker Claims model
  a2i: a2i *Amazon A2I | human review loop
  rev: users Reviewers
  s3: s3 Review results
---
model -> a2i : low-confidence predictions
a2i <-> rev
a2i -> s3
```

Why not the others:
- **A.** Comprehend custom classification labels text; it doesn't route predictions to human reviewers.
- **C.** Glue runs data integration and ETL jobs.
- **D.** Glacier is archival storage.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html>
</details>

**24. (Ordering)** A lender wants to manage bias throughout its model's life. Put these steps in order.
- A. Monitor the deployed model for bias drift in production
- B. Measure bias in the training dataset before training
- C. Train the model on the reviewed dataset
- D. Measure bias in the trained model's predictions before deployment

<details><summary>Answer</summary>

**B, C, D, A.** Bias management starts with checking the data, continues with checking the trained model's predictions, and continues after deployment, because real-world data can shift and introduce new bias. SageMaker Clarify covers the first two checks, and SageMaker Model Monitor integrates with Clarify to watch for bias drift.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-data-bias.html>
</details>

## Task 4.2: Recognize the importance of transparent and explainable models

**25.** A regulator asks a bank to use a model whose decision logic can be inspected directly. Which model type is MOST transparent by design?
- A. A deep neural network with 200 layers
- B. A large language model with billions of parameters
- C. A diffusion model that generates images
- D. A shallow decision tree with a few readable rules

<details><summary>Answer</summary>

**D.** Simple models such as shallow decision trees and linear regression are interpretable by design: people can read the rules or coefficients and see how inputs lead to outputs. Deep networks and LLMs are effectively black boxes and need post-hoc explanation tools.

Why not the others:
- **A.** A deep neural network's logic is spread across many layers and weights, which people can't read directly.
- **B.** LLMs are among the least transparent models.
- **C.** Diffusion models generate images and are also hard to interpret.

Resource: <https://aws.amazon.com/what-is/explainable-ai/>
</details>

**26.** A company wants a single place to document a model's intended uses, risk rating, training data details, evaluation results, and limitations, so that auditors and other teams can understand it. Which AWS feature should it use?
- A. Amazon CloudWatch dashboards
- B. AWS Secrets Manager
- C. Amazon Personalize
- D. Amazon SageMaker Model Cards

<details><summary>Answer</summary>

**D.** SageMaker Model Cards provide a structured way to document a model's purpose, intended uses, risk rating, training details, evaluation results, and other information, supporting transparency and governance throughout its lifecycle.

Why not the others:
- **A.** CloudWatch dashboards show operational metrics, not model documentation.
- **B.** Secrets Manager stores credentials.
- **C.** Personalize is a recommendation service.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html>
</details>

**27.** A bank uses a gradient-boosted model to approve loans. A rejected applicant asks why. The bank needs to show which features — such as income or debt ratio — most influenced that specific decision. Which capability provides this?
- A. SageMaker Clarify SHAP feature attributions per prediction
- B. Amazon Translate custom terminology for loan documents
- C. Amazon Bedrock prompt caching for the loan application
- D. AWS Budgets forecasts for the lending team's account

<details><summary>Answer</summary>

**A.** SageMaker Clarify explains model predictions with feature attributions based on SHAP (Shapley values), showing how much each feature contributed to an individual prediction or to the model's behavior overall.

```arch
row
  app: user Applicant record
  model: sagemaker Loan model
  clar: sagemaker *SageMaker Clarify | SHAP explanation
  off: users Loan officer
---
app -> model
model -> clar : prediction
clar -> off : top features
```

Why not the others:
- **B.** Translate terminology controls how words are translated.
- **C.** Prompt caching reduces generative AI cost and latency.
- **D.** Budgets forecasts AWS spending.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-explainability.html>
</details>

**28.** A company is comparing two foundation models for a customer-facing assistant. Besides accuracy, it wants evidence about how each model handles toxicity and robustness on its own prompts, documented in a report it can share with its risk committee. Which AWS capability supports this?
- A. AWS Trusted Advisor cost checks
- B. Amazon Bedrock model evaluations
- C. Amazon Rekognition celebrity recognition
- D. Amazon S3 Lifecycle rules

<details><summary>Answer</summary>

**B.** Bedrock model evaluations can measure metrics such as accuracy, robustness, and toxicity (automatic), use judge models for qualities such as harmfulness, or use human reviewers. The reports give stakeholders transparent evidence for model choices.

Why not the others:
- **A.** Trusted Advisor cost checks don't evaluate model behavior.
- **C.** Celebrity recognition is an image analysis feature.
- **D.** Lifecycle rules manage object storage classes and expiration.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html>
</details>

**29.** A university research group must be able to inspect a model's weights, review what data it was trained on, and confirm it may be used commercially by a spin-off company. What should the group look for when choosing a model?
- A. A closed model with no documentation, because secrecy improves safety
- B. Any model whose marketing page claims it is "transparent"
- C. An open-weight model with documented data and a suitable license
- D. The model with the highest benchmark score, regardless of license

<details><summary>Answer</summary>

**C.** Transparency depends on what can be inspected. Open-weight models, published data documentation, and clear licensing let the group examine the model and confirm it's allowed to use it as planned.

Why not the others:
- **A.** A closed, undocumented model fails the inspection requirement.
- **B.** Marketing claims aren't evidence of transparency.
- **D.** A high score doesn't help if the license forbids the intended use.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**30.** A hospital compares two models for predicting readmission risk. A logistic regression model is easy to explain but slightly less accurate. A deep neural network is 3% more accurate but hard to interpret. What trade-off is the hospital facing?
- A. Interpretability vs. performance
- B. Cost versus storage
- C. Latency versus throughput
- D. Region versus Availability Zone choice

<details><summary>Answer</summary>

**A.** More complex models often achieve higher accuracy but are less interpretable. Organizations must weigh how much explainability the use case needs (for example, for clinical or regulatory reasons) against gains in performance, and can add post-hoc explanation tools if they choose the complex model.

Why not the others:
- **B.** Storage isn't the issue being weighed.
- **C.** Latency and throughput aren't the difference described.
- **D.** Deployment location is unrelated.

Resource: <https://aws.amazon.com/what-is/explainable-ai/>
</details>

**31.** A security team asks the AI team not to publish the exact system prompts, guardrail rules, and filter thresholds of its public chatbot, even though the company values transparency. Why might this be reasonable?
- A. Transparency always lowers the accuracy of the model
- B. System prompts are always encrypted and can never be shared
- C. Revealing every safeguard detail could help attackers evade them
- D. Regulations forbid any kind of AI transparency to the public

<details><summary>Answer</summary>

**C.** There is a trade-off between transparency and safety. Being open about how and why AI is used builds trust, but revealing the exact details of safeguards can help attackers bypass them. Organizations can be transparent about policies and behavior without disclosing exploitable specifics.

Why not the others:
- **A.** Transparency doesn't by itself change accuracy.
- **B.** System prompts can be shared; the question is whether sharing them is wise.
- **D.** Regulations increasingly require transparency, not forbid it.

Resource: <https://aws.amazon.com/ai/responsible-ai/>
</details>

**32.** A medical imaging assistant shows doctors its suggested diagnosis. The team wants doctors to be able to flag incorrect suggestions easily so that the system can improve. Which human-centered design principle does this support?
- A. Removing humans from the loop entirely
- B. Feedback mechanisms for expert corrections
- C. Hiding the AI's role so doctors trust it more
- D. Increasing the model's temperature for each doctor

<details><summary>Answer</summary>

**B.** Human-centered explainable AI includes feedback mechanisms that let users challenge or correct AI outputs. Expert feedback improves the system and keeps people in control of high-stakes decisions.

Why not the others:
- **A.** In high-stakes settings, human oversight is a key safeguard.
- **C.** Hiding AI involvement undermines transparency and informed trust.
- **D.** Temperature is a generation setting, not a design principle.

Resource: <https://aws.amazon.com/what-is/explainable-ai/>
</details>

**33.** An online lender uses AI to make initial credit decisions. Which practice reflects AI decision transparency toward applicants?
- A. Sending every applicant the model's complete source code
- B. Never mentioning that AI was used, so that applicants don't worry
- C. Showing applicants the AWS Region where the model runs
- D. Telling applicants AI was used and explaining the main factors

<details><summary>Answer</summary>

**D.** Decision transparency means people know when AI is involved in decisions about them and get an understandable explanation of the main reasons, along with a way to ask questions or appeal.

Why not the others:
- **A.** Source code isn't meaningful to most applicants and may expose proprietary details.
- **B.** Concealing AI use undermines trust and may break regulations.
- **C.** Hosting location doesn't explain the decision.

Resource: <https://aws.amazon.com/what-is/explainable-ai/>
</details>

**34.** A team is designing an explainable AI experience for a tool that helps caseworkers prioritize benefit applications. Which TWO design choices follow human-centered principles? (Select TWO.)
- A. Show the key factors behind each priority score in plain language
- B. Make the AI's score final, with no way for caseworkers to override it
- C. Let caseworkers record disagreement with a score and feed that back for review
- D. Display only a numeric score with no context to keep the screen simple
- E. Hide that the score came from a model so that caseworkers treat it as their own

<details><summary>Answer</summary>

**A, C.** Human-centered explainable AI gives users understandable reasons for AI outputs and keeps humans in control, with channels for feedback and override.

Why not the others:
- **B.** Removing human override is risky for consequential decisions.
- **D.** A bare score with no explanation doesn't help users judge it.
- **E.** Concealing AI involvement undermines transparency.

Resource: <https://aws.amazon.com/what-is/explainable-ai/>
</details>

**35. (Matching)** A governance team is assigning AWS tools to responsible AI tasks. Match each task to the tool that supports it.
- Document a model's intended use, risks, and evaluation results => Amazon SageMaker Model Cards
- Measure dataset bias and explain individual predictions => Amazon SageMaker Clarify
- Block harmful topics and mask PII in a generative AI app => Amazon Bedrock Guardrails
- Send low-confidence predictions to human reviewers => Amazon Augmented AI (A2I)
- Detect bias drift in a deployed model over time => Amazon SageMaker Model Monitor
Extra choices: Amazon Polly | AWS Budgets

<details><summary>Answer</summary>

Model Cards support transparency and documentation. Clarify supports bias detection and explainability. Guardrails enforce safety and privacy policies in generative AI. A2I adds human review. Model Monitor (with Clarify) watches for bias drift in production. Polly (text-to-speech) and Budgets (cost tracking) aren't responsible AI tools.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html>
</details>
