# Domain 5: Security, Compliance, and Governance for AI Solutions (14%)

Guide page: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain5.html>

---

## Task 5.1: Explain methods to secure AI systems

**1.** A company allows several teams to use Amazon Bedrock. The marketing team should be able to invoke only one approved text model and nothing else in Bedrock. What is the BEST way to enforce this?
- A. Give the marketing team the AWS account root user credentials and ask them to be careful
- B. Attach an IAM policy that allows `bedrock:InvokeModel` only on that model's ARN
- C. Write "use only the approved model" in the application's system prompt
- D. Enable Amazon Macie on the account

<details><summary>Answer</summary>

**B.** IAM policies following least privilege can allow specific actions, such as invoking models, only on specific resources (the approved model's ARN). Any other model or Bedrock action is denied by default.

Why not the others:
- **A.** Sharing root credentials violates every IAM best practice.
- **C.** A prompt instruction can't enforce access control.
- **D.** Macie discovers sensitive data in S3; it doesn't control Bedrock access.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html>
</details>

**2.** A developer hard-coded an IAM user's access keys in a Lambda function that calls Amazon Bedrock. A security review flags this. What is the MOST secure fix?
- A. Move the access keys into an environment variable on the function
- B. Rotate the access keys every month and keep them in the code
- C. Give the function an execution role that can invoke the model
- D. Make the keys read-only by renaming the IAM user

<details><summary>Answer</summary>

**C.** An IAM execution role gives the function temporary, automatically rotated credentials with only the permissions it needs, so no long-term keys exist to leak.

```arch
cloud AWS Cloud
  fn: lambda Lambda function
  role: role *Execution role | bedrock:InvokeModel
  br: bedrock Amazon Bedrock
---
role -> fn : temporary credentials
fn -> br : InvokeModel
```

Why not the others:
- **A.** Environment variables still hold long-term keys that can leak.
- **B.** Rotation reduces exposure time but still leaves keys in code.
- **D.** Renaming a user doesn't change its permissions or remove the keys.

Resource: <https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html>
</details>

**3.** A bank fine-tunes a model on Amazon Bedrock using confidential data. Its security policy requires that the bank controls the encryption keys for the custom model and training artifacts, and can audit and revoke their use. What should it do?
- A. Use a customer managed AWS KMS key for the customization job and model
- B. Store the training data unencrypted so that the bank can read it more easily
- C. Ask the model provider to email the bank a copy of the encryption key
- D. Use Amazon Polly to encrypt the training data as audio

<details><summary>Answer</summary>

**A.** Bedrock encrypts data at rest by default, and customers can specify their own customer managed KMS keys for customization jobs, custom models, and other resources. With their own keys they control key policies, can audit key use in CloudTrail, and can disable or revoke access.

Why not the others:
- **B.** Unencrypted confidential data breaks the bank's policy.
- **C.** Model providers don't hold or share customers' keys, and emailing keys is insecure.
- **D.** Polly converts text to speech; it isn't an encryption service.

Resource: <https://docs.aws.amazon.com/kms/latest/developerguide/overview.html>
</details>

**4.** A security architect is reviewing data protection for a generative AI application on AWS. Which TWO controls protect data from interception or exposure? (Select TWO.)
- A. TLS encryption for data in transit to AWS services
- B. Encryption at rest with AWS KMS for stored data
- C. A higher temperature setting for the model in production
- D. Disabling AWS CloudTrail to reduce the number of logs
- E. Sharing a single IAM user among all developers

<details><summary>Answer</summary>

**A, B.** Encryption in transit (TLS) protects data moving over networks, and encryption at rest (with KMS keys) protects stored data such as training sets, documents, and embeddings.

Why not the others:
- **C.** Temperature affects randomness, not security.
- **D.** Disabling CloudTrail removes the audit trail.
- **E.** Shared IAM users break accountability and least privilege.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html>
</details>

**5.** A company plans to fine-tune a model on 2 TB of customer support transcripts stored in Amazon S3. It first needs to find which files contain personally identifiable information (PII), such as names, addresses, and credit card numbers. Which AWS service should it use?
- A. AWS Trusted Advisor
- B. Amazon CloudFront
- C. Amazon Lex
- D. Amazon Macie

<details><summary>Answer</summary>

**D.** Amazon Macie uses ML and pattern matching to discover and report sensitive data, such as PII and financial information, in Amazon S3, so the company can remove or mask it before training.

```arch
cloud AWS Cloud
  s3: s3 S3 bucket | support transcripts
  mac: macie *Amazon Macie | sensitive data discovery
  clean: databrew Mask or remove PII
  ft: bedrock Fine-tuning job
---
1. mac -> s3 : scan
2. mac -> clean : findings
3. clean -> ft : cleaned dataset
```

Why not the others:
- **A.** Trusted Advisor checks for best practices such as open S3 buckets but doesn't scan file contents for PII.
- **B.** CloudFront delivers content.
- **C.** Lex builds chatbots.

Resource: <https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html>
</details>

**6.** A healthcare company's application runs in private subnets with no internet access. It must call Amazon Bedrock without traffic leaving the AWS network or crossing the public internet. What should the company set up?
- A. A NAT gateway that sends Bedrock traffic over the public internet
- B. Amazon CloudFront in front of the Bedrock API
- C. An interface VPC endpoint for Amazon Bedrock using AWS PrivateLink
- D. A public IP address on every instance

<details><summary>Answer</summary>

**C.** AWS PrivateLink interface endpoints give private connectivity from a VPC to Bedrock: traffic stays on the AWS network, and endpoint policies can further restrict access.

```arch
cloud AWS Cloud
  vpc VPC
    private Private subnet
      app: ec2 Application
      ep: privatelink *Interface endpoint | Bedrock
  br: bedrock Amazon Bedrock
  inet: internet Internet
---
app -> ep
ep -> br : private connection
app -x-> inet : no internet route
```

Why not the others:
- **A.** A NAT gateway sends traffic to the public endpoint over the internet, which doesn't meet the requirement.
- **B.** CloudFront is a CDN for content delivery, not private service access.
- **D.** Public IPs expose instances and still route over the internet.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html>
</details>

**7. (Matching)** A company builds a generative AI application on Amazon Bedrock. Under the shared responsibility model, match each task to who is responsible for it.
- Physical security of the data centers that host Bedrock => AWS
- Patching and maintaining the infrastructure that serves the models => AWS
- Writing IAM policies that control who can invoke which models => Customer
- Classifying and protecting the data sent in prompts => Customer
- Configuring guardrails for the application's use case => Customer
- Isolating the model deployment from model providers' access => AWS

<details><summary>Answer</summary>

AWS secures the cloud: facilities, hardware, the managed service infrastructure, and the isolation of model deployment accounts. Customers secure what they put in the cloud: identities and permissions, their data, application configuration, and safeguards such as guardrails.

Resource: <https://aws.amazon.com/compliance/shared-responsibility-model/>
</details>

**8.** A company's AI agent must read a user's calendar in a third-party SaaS product on that user's behalf, using OAuth, without the agent's code ever storing long-term user credentials. Which AWS capability is designed for this?
- A. Amazon Bedrock prompt caching for the user's session
- B. Amazon S3 Object Lock on the user's calendar data
- C. Amazon Comprehend PII detection on the agent's prompts
- D. AgentCore Identity with an OAuth credential provider

<details><summary>Answer</summary>

**D.** AgentCore Identity provides identity and credential management for agents: it authenticates who calls the agent, and its credential providers (such as OAuth providers and API keys) let agents access AWS and third-party services on behalf of users, with credentials stored securely outside the agent code.

```arch
users: user Employee
row
  agent: agentcore Calendar agent
  idn: agentcore *AgentCore Identity | OAuth credential provider
  saas: internet SaaS calendar API
---
users -> agent : sign in
agent -> idn : get token for user
agent -> saas : call with user's token
```

Why not the others:
- **A.** Prompt caching reduces repeated token costs.
- **B.** Object Lock prevents objects from being deleted or overwritten.
- **C.** Comprehend detects PII in text but doesn't manage credentials.

Resource: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html>
</details>

**9.** A finance company's agent can call a `transfer_funds` tool through Amazon Bedrock AgentCore Gateway. Security requires that transfers above $10,000 are always blocked for agents acting for junior staff, regardless of what the model decides or how a prompt is worded. What should the company use?
- A. Policy in AgentCore, evaluating every tool call at the gateway
- B. A sentence in the system prompt asking the agent not to make large transfers
- C. A higher temperature so that the agent is less likely to choose the tool
- D. Amazon Polly to read each transfer aloud before it runs

<details><summary>Answer</summary>

**A.** Policy in AgentCore intercepts every tool call that passes through an AgentCore Gateway and evaluates it against deterministic policies (written in Cedar or authored in natural language) based on identity and tool input parameters. Enforcement happens outside the agent's code, so prompt manipulation can't bypass it.

```arch
row
  agent: agentcore Agent
  gw: agentcore AgentCore Gateway
  pol: policy *Policy engine | Cedar rules
  tool: lambda transfer_funds
---
agent -> gw : tool call
gw -> pol : evaluate
gw -> tool : only if permitted
```

Why not the others:
- **B.** Prompt instructions can be ignored or overridden by injection. They aren't enforcement.
- **C.** Temperature doesn't reliably prevent any action.
- **D.** Reading transfers aloud doesn't block them.

Resource: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html>
</details>

**10.** A public-facing assistant receives prompt injection attempts, and the company is worried that it might leak customers' personal data in responses. Which Amazon Bedrock feature addresses both concerns?
- A. Bedrock batch inference jobs that process requests asynchronously
- B. Bedrock Guardrails with prompt attack and sensitive information filters
- C. Bedrock Provisioned Throughput for the assistant's model
- D. Bedrock model distillation into a smaller, cheaper model

<details><summary>Answer</summary>

**B.** Guardrails detect prompt attacks such as injection and jailbreak attempts, and sensitive information filters block or mask PII in inputs and outputs, helping to prevent data leakage.

Why not the others:
- **A.** Batch inference is an asynchronous processing mode.
- **C.** Provisioned Throughput reserves capacity.
- **D.** Distillation creates smaller models.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html>
</details>

**11.** Compliance officers at an investment firm must be able to verify where every statement in an AI-generated research summary came from. Which design choice supports this?
- A. Raise the temperature so that the model explains itself more creatively
- B. Use RAG with source citations that link answers to documents
- C. Remove all metadata from the source documents before indexing
- D. Use a larger context window so that citations aren't needed

<details><summary>Answer</summary>

**B.** Source citation ties generated content to the specific documents that support it, so reviewers can verify claims. Bedrock Knowledge Bases return citations to the retrieved source chunks alongside responses.

Why not the others:
- **A.** Temperature doesn't produce verifiable sources.
- **C.** Stripping metadata makes it harder to trace answers to sources.
- **D.** Context window size doesn't show where statements came from.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html>
</details>

**12.** An auditor asks a company to show where the data used to train its fraud model came from and what transformations were applied before training. Which practice makes this possible?
- A. Deleting raw data immediately after each training job
- B. Training only on data that employees remember collecting
- C. Storing all training files with random names to save space
- D. Data lineage tracking and data cataloging across the pipeline

<details><summary>Answer</summary>

**D.** Data lineage records the origin of data and every transformation it went through. Data catalogs, such as the AWS Glue Data Catalog, describe datasets and their locations. Together they let auditors trace model inputs back to their sources.

Why not the others:
- **A.** Deleting raw data destroys the evidence auditors need.
- **B.** Memory isn't a reliable or auditable record.
- **C.** Random names make data harder to track.

Resource: <https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html>
</details>

**13.** A company wants each production model to have a record that documents its training data sources, intended uses, evaluation results, and risk rating, kept with the model for governance reviews. Which AWS feature fits?
- A. Amazon SageMaker Model Cards
- B. Amazon Route 53 health checks
- C. AWS Budgets
- D. Amazon Polly lexicons

<details><summary>Answer</summary>

**A.** SageMaker Model Cards document key model information, including training data details, intended uses, evaluation results, and risk ratings, supporting governance, audits, and documentation of data origins.

Why not the others:
- **B.** Route 53 health checks monitor endpoint availability.
- **C.** Budgets tracks costs.
- **D.** Polly lexicons customize pronunciation.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html>
</details>

**14.** Before using a large customer dataset to train a model, a data engineer wants to check it for missing values, duplicates, out-of-range values, and inconsistent formats. Which secure data engineering practice is this?
- A. Encrypting data in transit
- B. Prompt engineering for the model
- C. Assessing data quality before use
- D. Distilling a smaller model

<details><summary>Answer</summary>

**C.** Data quality assessment checks completeness, accuracy, consistency, and validity before data feeds a model. Tools such as AWS Glue DataBrew and AWS Glue Data Quality help profile and validate datasets.

Why not the others:
- **A.** Encryption protects data but doesn't check its quality.
- **B.** Prompt engineering designs model inputs at inference time.
- **D.** Distillation trains a smaller model.

Resource: <https://docs.aws.amazon.com/databrew/latest/dg/what-is.html>
</details>

**15.** A retailer wants to train a model on purchase history without exposing customers' real names, emails, and card numbers to the data science team. Which approach is a privacy-enhancing technique?
- A. Masking or tokenizing direct identifiers before training
- B. Copying the raw data to every data scientist's laptop
- C. Publishing the dataset to make the work more transparent
- D. Turning off encryption so that the data is easier to process

<details><summary>Answer</summary>

**A.** Privacy-enhancing techniques such as masking, tokenization, pseudonymization, and anonymization remove or replace direct identifiers, so models can learn patterns without exposing personal data.

Why not the others:
- **B.** Spreading raw data to laptops increases exposure.
- **C.** Publishing personal data is a privacy breach.
- **D.** Disabling encryption weakens protection.

Resource: <https://docs.aws.amazon.com/databrew/latest/dg/what-is.html>
</details>

**16.** A data lake in Amazon S3 holds training data for many ML teams. Each team may see only certain databases, tables, and columns, and the company wants to manage these permissions centrally. Which AWS service fits?
- A. Amazon Translate
- B. Amazon Rekognition
- C. AWS Lake Formation
- D. AWS Transform

<details><summary>Answer</summary>

**C.** AWS Lake Formation centrally manages fine-grained access control (database, table, column, row, and cell level) for data lakes, so each team only sees the training data it's authorized to use.

Why not the others:
- **A.** Translate converts text between languages.
- **B.** Rekognition analyzes images and video.
- **D.** AWS Transform helps migrate and modernize workloads.

Resource: <https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html>
</details>

**17.** A regulated company must prove that the dataset used to train a model wasn't altered after it was approved. Which practice supports data integrity?
- A. Allowing anyone in the company to overwrite files in the training bucket
- B. Versioning the dataset, recording checksums, and blocking overwrites
- C. Keeping only one copy of the data and no record of changes
- D. Converting the dataset to images before storing it

<details><summary>Answer</summary>

**B.** Integrity controls make tampering detectable or impossible: versioning keeps every revision, checksums detect changes, and write-once-read-many protection (such as S3 Object Lock) prevents approved data from being overwritten or deleted.

Why not the others:
- **A.** Unrestricted write access undermines integrity.
- **C.** Without change records, there's no way to prove the data is unchanged.
- **D.** Converting to images doesn't protect integrity.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html>
</details>

**18.** A financial regulator requires a company to keep records of the prompts sent to its generative AI application and the responses returned, plus a record of who called the Bedrock APIs. What should the company enable?
- A. Amazon Bedrock prompt caching for every request
- B. A lower temperature setting for every request
- C. Amazon Polly to read every response aloud to auditors
- D. Bedrock model invocation logging plus AWS CloudTrail

<details><summary>Answer</summary>

**D.** Model invocation logging captures request and response data for model invocations and delivers it to CloudWatch Logs and/or S3. CloudTrail records API calls (who did what, and when) for auditing. Logs should themselves be protected, because they may contain sensitive content.

```arch
cloud AWS Cloud
  app: lambda AI application
  br: bedrock Amazon Bedrock
  col [col]
    cwl: cloudwatch *CloudWatch Logs | invocation logs
    s3: s3 S3 bucket | invocation logs
    ct: cloudtrail *CloudTrail | API activity
---
app -> br : InvokeModel
br ~> cwl
br ~> s3
br ~> ct
```

Why not the others:
- **A.** Prompt caching speeds up requests; it doesn't create audit logs.
- **B.** Temperature has nothing to do with record keeping.
- **C.** Reading responses aloud creates no records.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html>
</details>

**19.** An assistant converts business users' questions into SQL queries that run against a reporting database. A tester gets the model to generate a `DROP TABLE` statement. Which security control should the team add?
- A. Increase the maximum output tokens so the model writes safer SQL
- B. Allow the model to run any SQL it generates, because models understand intent
- C. Remove logging so that the incident isn't recorded
- D. Validate model output before running it, using a read-only database role

<details><summary>Answer</summary>

**D.** Model output must be treated as untrusted input. Validating and filtering generated actions (for example, allowing only SELECT statements) and limiting the permissions of the identity that executes them prevent harmful actions even if the model is manipulated.

Why not the others:
- **A.** Longer output doesn't make generated SQL safer.
- **B.** Running unchecked model output is how injection becomes damage.
- **C.** Hiding incidents removes the audit trail and doesn't fix the risk.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html>
</details>

**20.** A company runs its model-serving containers on Amazon ECS and its pre-processing code on AWS Lambda. It wants continuous scanning of these workloads for known software vulnerabilities. Which AWS service should it use?
- A. Amazon Inspector
- B. Amazon Macie
- C. AWS Artifact
- D. Amazon Comprehend

<details><summary>Answer</summary>

**A.** Amazon Inspector automatically and continually scans Amazon EC2 instances, container images in Amazon ECR, and Lambda functions for software vulnerabilities and unintended network exposure, supporting vulnerability management for AI infrastructure.

Why not the others:
- **B.** Macie finds sensitive data in S3, not software vulnerabilities.
- **C.** Artifact provides compliance reports.
- **D.** Comprehend analyzes text.

Resource: <https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html>
</details>

**21.** A security team is listing threats specific to a customer-facing generative AI chatbot. Which TWO are security and privacy considerations for AI systems? (Select TWO.)
- A. Prompt injection that tries to override the chatbot's instructions
- B. Choosing a font for the chatbot's user interface
- C. Toxic or harmful content in model responses
- D. The color scheme of the company's logo
- E. The time zone shown in the chatbot's footer

<details><summary>Answer</summary>

**A, C.** AI-specific security and safety considerations include prompt injection, data leakage, toxic or harmful outputs, and logging and audit needs, alongside standard concerns such as encryption and access control.

Why not the others:
- **B.** Fonts are a design choice, not a security risk.
- **D.** Logo colors have no security impact.
- **E.** Time zone display isn't a security concern.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html>
</details>

**22.** A medical information assistant must reduce the risk of hallucinated answers reaching patients. Which TWO techniques help detect or prevent hallucinations? (Select TWO.)
- A. Ground answers with RAG on approved medical content and check them with a contextual grounding check
- B. Raise the temperature to its maximum value
- C. Validate outputs against trusted reference data before showing them
- D. Remove the system prompt to give the model more freedom
- E. Increase the number of answers generated per question and show all of them

<details><summary>Answer</summary>

**A, C.** Grounding answers in authoritative sources (RAG), checking grounding (Bedrock Guardrails contextual grounding checks), and validating outputs against trusted data are key ways to detect and reduce hallucinations.

Why not the others:
- **B.** Higher temperature increases randomness and the risk of errors.
- **D.** Removing instructions makes behavior less controlled.
- **E.** Showing many unverified answers increases the chance that patients see a wrong one.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html>
</details>

**23.** An insurance claims assistant produces a grounding or confidence score with each answer. How should the company use these scores to reduce the impact of hallucinations?
- A. Ignore the scores, because all answers should be treated the same
- B. Show only the answers with the lowest scores to customers
- C. Send answers below a threshold to a human reviewer instead
- D. Delete the scores to reduce storage costs

<details><summary>Answer</summary>

**C.** Confidence scoring lets the system act on uncertainty: low-scoring answers can be blocked, flagged, or routed to a person (for example, with Amazon A2I), while high-confidence answers proceed.

Why not the others:
- **A.** Ignoring scores throws away a useful safety signal.
- **B.** Low-confidence answers are the riskiest to show.
- **D.** Scores are small and valuable for quality monitoring.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html>
</details>

**24. (Ordering)** A company designs a secure request path for its RAG assistant. Put these steps in the order they happen for each user question.
- A. Generate a response from the question and retrieved passages
- B. Check the user's input with a guardrail for prompt attacks and denied topics
- C. Return the response to the user with source citations
- D. Retrieve relevant passages from the knowledge base
- E. Check the response with a guardrail for grounding and sensitive information

<details><summary>Answer</summary>

**B, D, A, E, C.** Input is screened first, so attacks never reach retrieval or the model. Then relevant context is retrieved, a response is generated, the output is checked for grounding and PII, and the approved response is returned with citations.

```arch
row [row]
  b: bedrock Input guardrail
  d: opensearch Retrieve
  a: bedrock Generate
  e: bedrock *Output guardrail
  c: users User | answer and citations
---
b -> d
d -> a
a -> e
e -> c
```

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html>
</details>

## Task 5.2: Recognize governance and compliance regulations for AI systems

**25.** A company's policy says that no Amazon SageMaker AI notebook instance may have direct internet access. The governance team wants to continuously evaluate all notebook instances against this rule and be alerted to any that don't comply. Which service fits?
- A. Amazon Polly voices
- B. AWS Config rules
- C. Amazon Personalize
- D. AWS Data Exchange

<details><summary>Answer</summary>

**B.** AWS Config records resource configurations and evaluates them against rules (including managed rules for SageMaker AI settings), flagging non-compliant resources and supporting automatic remediation.

```arch
cloud AWS Cloud
  nb: notebook SageMaker notebooks
  cfg: config *AWS Config | rules
  sns: sns Alert to governance team
---
cfg -> nb : evaluate configuration
cfg -> sns : non-compliant
```

Why not the others:
- **A.** Polly converts text to speech.
- **C.** Personalize builds recommendation systems.
- **D.** Data Exchange is a marketplace for third-party datasets.

Resource: <https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html>
</details>

**26.** A hospital's compliance officer needs AWS's own audit reports and certifications, such as SOC reports and ISO certifications, to support the hospital's assessment of AI workloads on AWS. Where can the officer get them?
- A. Amazon Inspector
- B. Amazon Macie
- C. AWS Artifact
- D. AWS Lambda

<details><summary>Answer</summary>

**C.** AWS Artifact is a self-service portal for AWS security and compliance reports (such as SOC reports and ISO certifications) and for accepting certain agreements.

Why not the others:
- **A.** Inspector scans the customer's workloads for vulnerabilities; it doesn't provide AWS's audit reports.
- **B.** Macie discovers sensitive data in S3.
- **D.** Lambda runs code.

Resource: <https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html>
</details>

**27.** An investigation needs to determine who changed a Bedrock guardrail configuration last Tuesday and from which IP address. Which AWS service provides this information?
- A. Amazon Translate
- B. AWS CloudTrail
- C. AWS Glue DataBrew
- D. Amazon Lex

<details><summary>Answer</summary>

**B.** CloudTrail records API calls made in an AWS account, including the identity of the caller, the time, the source IP address, and the request parameters, which provides an audit trail for configuration changes.

Why not the others:
- **A.** Translate converts text between languages.
- **C.** DataBrew prepares data.
- **D.** Lex builds chatbots.

Resource: <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html>
</details>

**28.** A small company wants automated recommendations about security gaps, cost optimization, and service limits across the AWS account that hosts its AI workloads — for example, S3 buckets with open access or underused resources. Which service provides these best-practice checks?
- A. AWS Trusted Advisor
- B. Amazon Rekognition
- C. Amazon Nova
- D. Amazon Transcribe

<details><summary>Answer</summary>

**A.** Trusted Advisor inspects an AWS environment and recommends improvements across cost optimization, performance, security, fault tolerance, service limits, and operational excellence.

Why not the others:
- **B.** Rekognition analyzes images and video.
- **C.** Nova is a family of foundation models.
- **D.** Transcribe converts speech to text.

Resource: <https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html>
</details>

**29. (Matching)** A governance team is assigning AWS services to compliance needs for its AI platform. Match each need to the service.
- Continuously evaluate resource settings against internal rules => AWS Config
- Scan container images and Lambda functions for vulnerabilities => Amazon Inspector
- Download AWS's compliance reports for auditors => AWS Artifact
- Record who made which API calls and when => AWS CloudTrail
- Get best-practice recommendations on security and cost => AWS Trusted Advisor
Extra choices: Amazon Polly | Amazon Personalize

<details><summary>Answer</summary>

Config evaluates configuration compliance. Inspector manages vulnerabilities. Artifact provides AWS audit reports. CloudTrail provides the API audit trail. Trusted Advisor recommends improvements. Polly and Personalize aren't governance services.

Resource: <https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html>
</details>

**30.** A company's policy says that logs containing chat prompts must be kept for 90 days for investigations and then deleted automatically. The logs are stored in Amazon S3. Which approach implements this data lifecycle rule?
- A. A reminder for an employee to delete old files manually each quarter
- B. Raising the model's temperature after 90 days
- C. Copying the logs to more buckets to make them easier to find
- D. An S3 Lifecycle configuration that expires the log objects after 90 days

<details><summary>Answer</summary>

**D.** S3 Lifecycle rules can transition objects between storage classes and expire (delete) them after a set time, enforcing retention policies automatically and consistently.

Why not the others:
- **A.** Manual deletion is error-prone and hard to audit.
- **B.** Temperature has nothing to do with data retention.
- **C.** More copies make retention harder to enforce.

Resource: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>
</details>

**31.** A company operating in the EU has a data residency policy: training data and AI workloads must stay in approved EU Regions. It wants a preventive control across all accounts in AWS Organizations. What should it use?
- A. A service control policy (SCP) that denies other Regions
- B. A note in each team's wiki asking them to use EU Regions
- C. Amazon Polly configured with a European voice
- D. A larger model with multilingual support

<details><summary>Answer</summary>

**A.** SCPs set maximum permissions across accounts in an organization. A Region-restriction SCP denies requests to unapproved Regions, preventing data and workloads from being created elsewhere.

Why not the others:
- **B.** A wiki note isn't an enforced control.
- **C.** A voice's accent has nothing to do with where data is stored.
- **D.** Multilingual capability doesn't control data location.

Resource: <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html>
</details>

**32.** A team wants ongoing visibility into how its Amazon Bedrock application behaves in production: invocation counts, latency, errors, throttling, and token usage, with alarms when values cross thresholds. Which service provides this monitoring?
- A. AWS Artifact
- B. Amazon Textract
- C. AWS Data Exchange
- D. Amazon CloudWatch

<details><summary>Answer</summary>

**D.** Amazon Bedrock publishes metrics such as invocations, latency, errors, throttles, and input and output token counts to CloudWatch, where teams can build dashboards and alarms as part of ongoing monitoring and observation.

Why not the others:
- **A.** Artifact provides compliance documents.
- **B.** Textract extracts text from documents.
- **C.** Data Exchange is for finding and subscribing to third-party data.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring.html>
</details>

**33. (Matching)** A security team uses the Generative AI Security Scoping Matrix to classify projects. Match each project to its scope.
- Employees use a public consumer chat app for brainstorming => Scope 1: Consumer app
- Staff use a third-party SaaS tool with built-in generative AI features => Scope 2: Enterprise app
- Developers build an app that calls a foundation model through Amazon Bedrock as-is => Scope 3: Pre-trained models
- The team customizes a Bedrock model with its own data through fine-tuning => Scope 4: Fine-tuned models
- Researchers train their own model from scratch on company data => Scope 5: Self-trained models

<details><summary>Answer</summary>

The scoping matrix classifies generative AI use by how much the organization owns: from using public consumer services (Scope 1) and enterprise applications (Scope 2), to building on pre-trained models (Scope 3), fine-tuning them (Scope 4), and training models from scratch (Scope 5). Security and governance responsibilities grow with each scope.

Resource: <https://aws.amazon.com/ai/security/generative-ai-scoping-matrix/>
</details>

**34.** A company is setting up governance processes for its growing number of AI applications. Which TWO practices belong in that process? (Select TWO.)
- A. A regular review cadence to reassess each AI system's risk
- B. Allowing each team to deploy AI systems with no documentation or review
- C. Required training on AI policies for teams that build or use AI
- D. Removing all logging to protect users' privacy
- E. Reviewing an AI system only once, before its first deployment

<details><summary>Answer</summary>

**A, C.** Effective AI governance includes defined policies, periodic reviews on a set cadence, review strategies (for example, risk-based depth), transparency standards, and required training so people know and follow the rules.

Why not the others:
- **B.** No documentation or review defeats governance.
- **D.** Logging is needed for audits. Privacy is better handled by protecting and minimizing logs.
- **E.** Systems, data, and risks change, so a single review isn't enough.

Resource: <https://docs.aws.amazon.com/whitepapers/latest/aws-caf-for-ai/aws-caf-for-ai.html>
</details>

**35.** A large enterprise has dozens of teams experimenting with generative AI in different ways, with no consistent rules on acceptable use, data handling, or approval. What should it establish FIRST?
- A. A ban on all logging so that experiments run faster
- B. A rule that every team must use the largest available model
- C. An AI governance framework with policies, roles, and approvals
- D. A single shared IAM user for all of the AI experiments

<details><summary>Answer</summary>

**C.** A governance framework defines acceptable use, data handling, risk assessment, roles and responsibilities, and approval workflows, giving teams consistent rules while enabling innovation. Frameworks such as the AWS Cloud Adoption Framework for AI and the Generative AI Security Scoping Matrix help structure it.

Why not the others:
- **A.** Removing logs harms auditability.
- **B.** Model size isn't a governance policy and often raises cost without benefit.
- **D.** Shared IAM users break accountability and least privilege.

Resource: <https://docs.aws.amazon.com/whitepapers/latest/aws-caf-for-ai/aws-caf-for-ai.html>
</details>
