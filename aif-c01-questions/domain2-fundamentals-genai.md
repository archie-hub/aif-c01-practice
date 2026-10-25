# Domain 2: Fundamentals of GenAI (24%)

Guide page: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain2.html>

---

## Task 2.1: Explain the basic concepts of generative AI (GenAI)

**1.** A finance analyst sees that the company's generative AI bill is calculated per "token." What is a token?
- A. A unit of text, such as a word or part of a word, that the model reads and generates
- B. A security credential that each user must present before calling the model
- C. A single training example in the dataset that was used to pre-train the model
- D. A fixed monthly license fee that covers unlimited requests to one model

<details><summary>Answer</summary>

**A.** Models break text into tokens, which are words, parts of words, or punctuation. Both the input (prompt) and the output (completion) are measured in tokens, and on-demand pricing for most text models is charged per input and output token.

Why not the others:
- **B.** Credentials such as IAM credentials control access to the API. They aren't the unit the model processes or bills.
- **C.** Training examples are records in a dataset. A token is a much smaller unit of text.
- **D.** On-demand token pricing is pay-per-use, not a flat license fee.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/key-definitions.html>
</details>

**2.** A company is building a question-answering assistant over 5,000 product manuals, some of them 300 pages long. Before creating embeddings, the engineer splits each manual into passages of a few hundred tokens. Why is this chunking step needed?
- A. Chunking encrypts each manual so that the model can't read confidential content
- B. Chunking translates every manual into the model's preferred language before search
- C. Chunking removes the need for an embeddings model because each chunk is searched by file name
- D. Smaller passages can be retrieved precisely and fit in the model's context window

<details><summary>Answer</summary>

**D.** Chunking splits long documents into smaller passages. Each chunk gets its own embedding, so a search returns only the most relevant passages instead of whole manuals, and the retrieved text fits inside the model's limited context window. Chunk size and overlap affect retrieval quality.

Why not the others:
- **A.** Chunking doesn't encrypt anything. Encryption is handled by services such as AWS KMS.
- **B.** Chunking splits text; it doesn't translate it.
- **C.** Chunks are still converted to embeddings so they can be searched by meaning, not by file name.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html>
</details>

**3.** A developer explains that the search feature converts each support article into an "embedding." What is an embedding?
- A. A compressed ZIP copy of the article stored inside the foundation model's weights
- B. A numerical vector that captures the text's meaning, so similar texts are close together
- C. A list of the article's keywords sorted alphabetically for exact-match lookups later
- D. An HTML snippet that embeds the article into the help center's web pages

<details><summary>Answer</summary>

**B.** An embedding model turns text (or images) into a vector of numbers that captures its semantic meaning. Texts with similar meanings produce vectors that are close together, which enables semantic search, clustering, and Retrieval Augmented Generation (RAG).

Why not the others:
- **A.** Embeddings aren't compressed copies of documents, and they aren't stored in the generating model's weights.
- **C.** Keyword lists support lexical (exact-match) search. Embeddings capture meaning, so "refund" can match "money back."
- **D.** Embedding in the ML sense isn't about placing content in HTML pages.

Resource: <https://aws.amazon.com/what-is/embeddings-in-machine-learning/>
</details>

**4.** A customer types "my package never showed up" into a help center search box. The best article is titled "Missing or undelivered orders," which shares no words with the query. Which approach finds that article?
- A. A SQL query that uses `LIKE '%package%'` against the article titles
- B. Sorting all articles by publication date and returning the newest one
- C. Embedding the query and articles and running a vector similarity search
- D. Asking the customer to rephrase the question using the exact words from the titles

<details><summary>Answer</summary>

**C.** Semantic search converts both the query and the articles into embeddings and returns the articles whose vectors are nearest to the query's vector. Because embeddings encode meaning, the query matches the article even though no words overlap.

```arch
users: users Customer
cloud AWS Cloud
  app: lambda Search API
  emb: bedrock Embeddings model | Amazon Bedrock
  vs: opensearch *Vector store | k-NN search
---
1. users -> app : query
2. app -> emb : embed query
3. app <-> vs : nearest articles
```

Why not the others:
- **A.** Keyword matching fails when the query and the article use different words for the same idea.
- **B.** Date order has nothing to do with relevance to the question.
- **D.** Making users guess the right words is the problem semantic search solves.

Resource: <https://aws.amazon.com/what-is/vector-databases/>
</details>

**5.** Most modern large language models use the transformer architecture. What key mechanism lets transformers understand how words in a long passage relate to one another?
- A. Self-attention, which weighs how relevant each token is to every other token in the input
- B. A lookup table that stores the dictionary definition of every word in the vocabulary
- C. A decision tree that splits sentences into grammatical parts one rule at a time
- D. Clustering, which groups the words of a sentence before any text is generated

<details><summary>Answer</summary>

**A.** The self-attention mechanism lets a transformer consider all tokens in the input at once and learn how strongly each one relates to the others, capturing context and long-range dependencies. It also allows training to run in parallel, which made very large models practical.

Why not the others:
- **B.** Transformers learn contextual representations; a static dictionary can't capture that "bank" means different things in different sentences.
- **C.** Decision trees are a classic ML algorithm, not the core of transformer models.
- **D.** Clustering is an unsupervised technique for grouping data. It isn't how transformers process text.

Resource: <https://aws.amazon.com/what-is/transformers-in-artificial-intelligence/>
</details>

**6.** What distinguishes a foundation model (FM) from a traditional ML model built for one task?
- A. An FM is trained only on one company's labeled data and supports a single prediction
- B. An FM is pre-trained on broad, large-scale data and can be adapted to many different tasks
- C. An FM is a rules engine that must be programmed by hand for each new use case
- D. An FM can't be fine-tuned or prompted and is used exactly as originally trained

<details><summary>Answer</summary>

**B.** Foundation models are very large models pre-trained, usually with self-supervised learning, on broad data. They serve as a general-purpose base that can be adapted through prompting, RAG, or fine-tuning to tasks such as summarization, Q&A, classification, and code generation.

Why not the others:
- **A.** That describes a traditional task-specific model, not a foundation model.
- **C.** FMs learn from data; they aren't programmed with hand-written rules.
- **D.** FMs are designed to be adapted through prompts and, often, customization.

Resource: <https://aws.amazon.com/what-is/foundation-models/>
</details>

**7.** An insurance company wants a model that looks at a photo of a damaged car and a short text description from the customer, then writes a first-draft damage summary. What kind of model is required?
- A. A text-only model, because the photo can be ignored once the customer has written a description
- B. A clustering model that groups photos of cars by color before writing anything
- C. A multimodal model that accepts both image and text input and generates text
- D. A speech recognition model that converts the photo into audio and then into text

<details><summary>Answer</summary>

**C.** Multimodal models can take more than one type of input (for example, images and text) and reason over them together. Several FMs on Amazon Bedrock, such as Amazon Nova Lite and Pro, accept image and text input and produce text output.

Why not the others:
- **A.** A text-only model can't see the damage in the photo, which is the key evidence.
- **B.** Clustering photos by color doesn't analyze damage or write a summary.
- **D.** Photos aren't audio, and speech recognition doesn't interpret images.

Resource: <https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html>
</details>

**8.** A design agency uses a model that creates new marketing images from text prompts. The model starts from random noise and refines it step by step into a picture that matches the prompt. What type of model is this?
- A. A regression model
- B. A recommendation model
- C. A speech synthesis model
- D. A diffusion model

<details><summary>Answer</summary>

**D.** Diffusion models learn to reverse a process that gradually adds noise to images. At generation time they start from noise and denoise it over many steps, guided by the text prompt, to produce a new image. Many image generation models, such as Stable Diffusion, work this way.

Why not the others:
- **A.** Regression models predict numeric values; they don't generate images.
- **B.** Recommendation models rank existing items for users.
- **C.** Speech synthesis models (text-to-speech) generate audio, not images.

Resource: <https://aws.amazon.com/what-is/generative-ai/>
</details>

**9. (Matching)** A new team member is building a glossary of generative AI terms. Match each term to its definition.
- The basic unit of text that a model reads and produces => Token
- A vector of numbers that represents the meaning of a piece of content => Embedding
- Splitting a long document into smaller passages before indexing it => Chunking
- The maximum amount of input and output text the model can consider at once => Context window
- The instructions and input text sent to a model to get a response => Prompt
Extra choices: Hyperparameter | Fine-tuning

<details><summary>Answer</summary>

Tokens are the units models process and bill by. Embeddings represent meaning as vectors for semantic search. Chunking splits documents for retrieval. The context window limits how many tokens the model can handle in a single request. A prompt is the input given to the model. Hyperparameters are training settings, and fine-tuning is further training of a model, so neither fits these definitions.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/key-definitions.html>
</details>

**10.** A media company is collecting ideas for generative AI projects. Which TWO ideas are good uses of generative AI? (Select TWO.)
- A. Drafting first versions of article summaries that editors review before publishing
- B. Calculating each employee's exact payroll tax from published tax tables
- C. Generating code suggestions that help developers write data-processing scripts faster
- D. Storing the official, legally binding record of each subscriber's contract
- E. Counting the exact number of rows in a database table each night

<details><summary>Answer</summary>

**A, C.** Generative AI creates new content such as text, summaries, images, and code. Draft summaries and code suggestions are strong use cases, especially with human review.

Why not the others:
- **B.** Exact tax calculations need deterministic code. A generative model's output could vary or be wrong.
- **D.** A legal system of record needs reliable storage, not generated content.
- **E.** Counting rows is a simple deterministic query.

Resource: <https://aws.amazon.com/what-is/generative-ai/>
</details>

**11.** An online furniture store wants to create lifestyle images that show its sofas in many different room styles, without paying for a new photo shoot each time. Which generative AI capability fits BEST?
- A. A speech-to-text model that transcribes interior designers' ideas
- B. A sentiment analysis model that scores how customers feel about each sofa
- C. An image generation model, such as Amazon Nova Canvas, guided by text prompts
- D. A forecasting model that predicts how many sofas will sell next quarter

<details><summary>Answer</summary>

**C.** Image generation models create new images from text prompts and can use input images for editing tasks such as changing backgrounds. Amazon Nova Canvas on Amazon Bedrock is one example.

Why not the others:
- **A.** Transcribing ideas produces text, not images.
- **B.** Sentiment analysis measures opinions; it doesn't create images.
- **D.** Forecasting predicts numbers; it doesn't generate marketing images.

Resource: <https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html>
</details>

**12. (Ordering)** An AI lab is explaining the lifecycle of a foundation model to its investors. Put these stages in order, from first to last.
- A. Fine-tune the model for specific tasks and behaviors
- B. Evaluate the model against benchmarks and safety criteria
- C. Select and prepare large, broad training data
- D. Deploy the model and collect user feedback
- E. Pre-train the model on the prepared data

<details><summary>Answer</summary>

**C, E, A, B, D.** The FM lifecycle starts with selecting and curating data, then pre-training on it (the most expensive step), then fine-tuning for instruction following or specific domains, then evaluating quality and safety, and finally deploying the model and gathering feedback that informs future improvements.

Resource: <https://aws.amazon.com/what-is/foundation-models/>
</details>

**13.** After launching a generative AI writing assistant, a company adds thumbs-up and thumbs-down buttons to every response and reviews the results each month. Which stage of the foundation model lifecycle does this support?
- A. Feedback, which guides prompt changes, evaluation, and future fine-tuning
- B. Pre-training, because the buttons directly change the model's weights in real time
- C. Data selection for pre-training a brand-new foundation model from scratch
- D. Deployment, because the buttons decide which AWS Region hosts the model

<details><summary>Answer</summary>

**A.** The feedback stage collects real-world signals about output quality. Those signals inform prompt improvements, new evaluation datasets, and future fine-tuning (for example, preference data for RLHF). They don't change the model instantly.

Why not the others:
- **B.** User ratings don't modify weights in real time. Any retraining is a separate, deliberate step.
- **C.** The company isn't building a new FM from scratch. It's improving its deployed application.
- **D.** Ratings have nothing to do with choosing a hosting Region.

Resource: <https://aws.amazon.com/what-is/reinforcement-learning-from-human-feedback/>
</details>

**14.** A support chatbot built on Amazon Bedrock with on-demand pricing costs more than expected. Logs show that every request sends a 6,000-token policy document in the prompt, and answers average 150 tokens. What is the MOST likely reason for the high cost?
- A. On-demand pricing charges a fixed fee per request, regardless of how many tokens are used
- B. Input tokens are billed too, so the document sent with each request drives cost
- C. Bedrock charges only for output tokens, so the short answers must be priced at a premium
- D. The model is retrained after every request, and retraining is billed per hour

<details><summary>Answer</summary>

**B.** On-demand token pricing charges for both input and output tokens. Sending a 6,000-token document with every request means each call pays for thousands of input tokens. Options include retrieving only relevant passages (RAG), shortening the prompt, or using prompt caching for the repeated prefix.

Why not the others:
- **A.** On-demand pricing for text models is per token, not a flat per-request fee.
- **C.** Input tokens are billed as well as output tokens. Output tokens usually cost more per token, but 150 tokens per answer is small.
- **D.** Invoking a model doesn't retrain it.

Resource: <https://aws.amazon.com/bedrock/pricing/>
</details>

**15.** A team wants to lower the per-request cost of a text-generation feature that uses on-demand, token-based pricing. Which TWO changes directly reduce the number of billed tokens? (Select TWO.)
- A. Remove repeated, unnecessary instructions and examples from the prompt
- B. Increase the temperature so the model writes more creative answers
- C. Set a lower maximum output length that still fits the answers users need
- D. Send the same request twice and keep the better of the two answers
- E. Switch the IAM role used by the application to one with more permissions

<details><summary>Answer</summary>

**A, C.** Billing depends on input and output tokens. Trimming the prompt reduces input tokens, and capping the response length reduces output tokens.

Why not the others:
- **B.** Temperature changes randomness, not length or cost.
- **D.** Sending each request twice doubles the tokens and the cost.
- **E.** IAM permissions control access; they have no effect on token counts.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html>
</details>

**16.** A product team notices that responses from its generative AI feature take noticeably longer when users paste long documents into the prompt and ask for detailed answers. What explains this?
- A. The model downloads the pasted documents from the internet before answering
- B. Long prompts force the service to retrain the model on the new documents first
- C. Latency depends only on network distance, so prompt length can't be the cause
- D. More input and output tokens mean more processing, so latency rises

<details><summary>Answer</summary>

**D.** The model has to process every input token and generate output one token at a time, so longer inputs and longer outputs both increase response time as well as cost. Shorter prompts, tighter output limits, smaller models, and prompt caching can reduce latency.

Why not the others:
- **A.** Content in the prompt is sent with the request. The model doesn't fetch it from the internet.
- **B.** Inference never retrains the model.
- **C.** Network distance matters, but token count is a major factor in generation time.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html>
</details>

**17.** An architect says the team should focus on "context engineering" for its enterprise assistant. What does context engineering mean?
- A. Deciding what fills the model's context window: instructions, retrieved data, memory, and tool results
- B. Choosing the AWS Region and instance type that host the foundation model for each request
- C. Rewriting the model's source code and weights so that it understands the company's business context
- D. Encrypting the prompt and the response so that no other application context can read them

<details><summary>Answer</summary>

**A.** Context engineering is the practice of selecting, structuring, and managing everything that goes into the model's context window for each request: system instructions, relevant retrieved documents, conversation history and memory, tool definitions and results, and examples. Good context improves accuracy and reduces cost.

Why not the others:
- **B.** Region and instance choices are deployment decisions, not context engineering.
- **C.** Context engineering works with the model's inputs, not its code or weights.
- **D.** Encryption protects data but doesn't decide what the model sees.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering-guidelines.html>
</details>

**18.** An agent that helps employees with IT tickets gets slower, more expensive, and less accurate as a conversation goes on. The team finds it sends the full history, every tool output, and 40 policy documents with every request. Which change reflects good context engineering?
- A. Switch to a model with a larger context window so that even more history can be included
- B. Retrieve only the relevant policies and summarize or trim older history and tool output
- C. Remove the system instructions to make room for all the documents
- D. Ask employees to start a new conversation every time they send a message

<details><summary>Answer</summary>

**B.** Context engineering keeps the context focused: retrieve only relevant documents, summarize or drop stale history, and keep the tool output the model actually needs. Irrelevant context costs tokens, adds latency, and can distract the model from what matters.

Why not the others:
- **A.** A larger window allows more tokens but doesn't fix the cost, latency, and distraction caused by irrelevant content.
- **C.** System instructions guide the agent's behavior. Removing them would make answers worse.
- **D.** Starting over every message loses useful context and frustrates employees.

Resource: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html>
</details>

**19. (Ordering)** A developer gives a model a `get_order_status` tool. A customer asks, "Where is order 1182?" Put the steps of this tool-use interaction in order.
- A. The model responds with a request to call `get_order_status` for order 1182
- B. The application sends the customer's question and the tool definition to the model
- C. The model writes the final answer to the customer using the tool's result
- D. The application runs the tool and returns the result to the model

<details><summary>Answer</summary>

**B, A, D, C.** In tool use (function calling), the application describes the available tools in the request. The model decides a tool is needed and returns a structured tool call, the application (not the model) executes it, and the model uses the returned data to compose its final response.

```arch
row
  users: user Customer
  app: app Application
  col [col]
    fm: bedrock Foundation model
    tool: lambda get_order_status
---
users <-> app : question and answer
app <-> fm : tool request and result
app -> tool : run tool
```

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>
</details>

**20.** A company wants its AI agents to connect to internal systems such as a ticketing tool, a wiki, and a database, without writing a different custom integration for each agent framework. Which open standard is designed for this?
- A. Structured Query Language (SQL), which lets agents query any system with the same commands
- B. Simple Mail Transfer Protocol (SMTP), which agents use to email each system for data
- C. Speech Synthesis Markup Language (SSML), which describes tools in a format that models can speak
- D. Model Context Protocol (MCP), which standardizes how AI applications connect to external tools and data

<details><summary>Answer</summary>

**D.** MCP is an open protocol that standardizes how AI applications and agents discover and call tools, resources, and prompts exposed by MCP servers. A system wrapped once as an MCP server can be used by any MCP-compatible client or agent.

Why not the others:
- **A.** SQL queries relational databases. It doesn't describe tools to agents or connect to non-database systems.
- **B.** SMTP sends email. It's not a tool integration standard for agents.
- **C.** SSML controls speech synthesis output, for example in Amazon Polly.

Resource: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html>
</details>

**21.** A bank builds a customer-service assistant from several agents: one handles card disputes, one handles mortgages, and one handles account updates. A fourth agent reads each request, decides which specialist should handle it, and combines their answers. Which multi-agent pattern is this?
- A. A single-agent pattern with one very long prompt that covers every topic
- B. A batch inference pattern, in which requests are collected and processed once a day
- C. A supervisor (orchestrator) pattern, in which one agent routes work to specialist agents
- D. A clustering pattern, in which agents group customers into segments

<details><summary>Answer</summary>

**C.** In a supervisor or orchestrator pattern, a coordinating agent breaks down the request, delegates subtasks to specialist agents (for example, using agents as tools), and assembles the results. Specialists stay focused, which improves accuracy and makes each one easier to maintain.

```arch
users: users Customers
cloud AWS Cloud [col]
  sup: agentcore *Supervisor agent
  row
    a1: agentcore Card disputes
    a2: agentcore Mortgages
    a3: agentcore Account updates
---
users -> sup : request
sup -> a1
sup -> a2
sup -> a3
```

Why not the others:
- **A.** One giant prompt is the opposite of a multi-agent design and tends to be harder to control.
- **B.** Batch inference is an inference mode for large offline jobs, not a way of coordinating agents.
- **D.** Clustering is unsupervised ML for grouping data.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html>
</details>

**22.** A travel agent built with Amazon Bedrock AgentCore should remember what a traveler said earlier in the same conversation, and also remember the traveler's seat and meal preferences across future trips. Which capability supports this?
- A. Prompt caching, which stores the model's answers so that it never needs to generate new ones
- B. A larger context window, which keeps every past trip in each request forever
- C. AgentCore Memory, with short-term memory for the session and long-term memory across sessions
- D. Batch inference, which processes all of a traveler's trips together each night

<details><summary>Answer</summary>

**C.** AgentCore Memory provides short-term memory for multi-turn conversations within a session and long-term memory that persists insights such as user preferences across sessions, so agents stay context-aware without resending everything.

```arch
users: user Traveler
cloud AWS Cloud
  rt: agentcore Travel agent | AgentCore Runtime
  mem: agentcore *AgentCore Memory | short and long term
---
users <-> rt : conversation
rt <-> mem : store and recall
```

Why not the others:
- **A.** Prompt caching reuses repeated prompt prefixes to save cost and latency. It doesn't store user preferences.
- **B.** Resending every past trip in each request is expensive, slow, and eventually exceeds any context window.
- **D.** Batch inference is for offline bulk processing, not conversational memory.

Resource: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html>
</details>

**23.** A company's invoice-approval process always follows the same five steps in the same order, and auditors require it to behave identically every time. A developer proposes a fully autonomous agent that decides the steps on its own. What is the BEST recommendation?
- A. Use the autonomous agent, because agents are always more accurate than fixed workflows
- B. Remove all automation and process every invoice by hand to satisfy the auditors
- C. Use a diffusion model to generate a new approval process for each incoming invoice
- D. Use a defined workflow for the fixed steps, calling a model only where judgment is needed

<details><summary>Answer</summary>

**D.** When steps are known and must be predictable, workflow orchestration (for example, AWS Step Functions or Amazon Bedrock Flows) gives deterministic control, with model calls inserted only for tasks that need language understanding. Autonomous agents are better when the path to the goal can't be defined in advance.

Why not the others:
- **A.** Autonomous agents add flexibility, not guaranteed accuracy, and their paths can vary, which conflicts with the audit requirement.
- **B.** Manual processing isn't needed. A deterministic workflow satisfies the auditors and still automates the work.
- **C.** Diffusion models generate images, and a different process per invoice is the opposite of what's required.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html>
</details>

**24. (Matching)** An architecture review covers the building blocks of an agentic application. Match each description to the concept.
- An open standard that exposes external tools and data to agents in a consistent way => Model Context Protocol (MCP)
- The model returns a structured request for the application to call a function => Tool use
- Keeping track of what was said earlier in the current conversation => Short-term memory
- Remembering a user's preferences across separate sessions => Long-term memory
- An agent that breaks a task into parts and delegates them to specialist agents => Orchestrator agent
Extra choices: Diffusion | Tokenization

<details><summary>Answer</summary>

MCP standardizes tool and data connections. Tool use (function calling) lets the model ask the application to run code. Short-term memory holds the current session's context, and long-term memory persists information across sessions. An orchestrator (supervisor) agent coordinates specialist agents in a multi-agent system. Diffusion is an image generation technique and tokenization splits text into tokens, so neither matches.

Resource: <https://aws.amazon.com/what-is/ai-agents/>
</details>

**25.** A team building with Strands Agents wants a main agent that can call a research agent and a writing agent the same way it calls any other tool, then combine their outputs. Which multi-agent pattern does this describe?
- A. Fine-tuning, in which the research agent's weights are merged into the writing agent
- B. Agents as tools, in which specialist agents are wrapped as tools for an orchestrating agent
- C. Batch transform, in which both agents score the same dataset offline
- D. Prompt caching, in which the agents share a cached copy of each other's answers

<details><summary>Answer</summary>

**B.** In the agents-as-tools pattern, specialist agents are exposed as callable tools. The orchestrator decides when to call each one, passes it a task, and uses the result. Strands Agents also supports other multi-agent patterns, such as swarm and graph.

Why not the others:
- **A.** Fine-tuning changes a model's weights. It isn't a way for agents to cooperate.
- **C.** Batch transform is a SageMaker AI offline inference feature.
- **D.** Prompt caching reduces repeated input cost; it doesn't coordinate agents.

Resource: <https://strandsagents.com/latest/>
</details>

## Task 2.2: Understand the capabilities and limitations of GenAI for solving business problems

**26.** A consulting firm uses one foundation model to draft proposals, summarize meeting notes, translate emails, and answer staff questions. Which advantage of generative AI does this demonstrate MOST directly?
- A. Adaptability, because a single model handles many different tasks without separate training
- B. Determinism, because the model always returns identical answers to identical prompts
- C. Interpretability, because the model can explain exactly which weights produced each answer
- D. Guaranteed accuracy, because foundation models don't make factual mistakes

<details><summary>Answer</summary>

**A.** Foundation models are general-purpose. One model can be steered to many tasks with prompts, which is a key advantage over training a separate model per task.

Why not the others:
- **B.** Generative models are typically nondeterministic. Determinism isn't one of their advantages.
- **C.** Interpretability is a known weakness of large models, not a strength.
- **D.** FMs can hallucinate. Accuracy is never guaranteed.

Resource: <https://aws.amazon.com/what-is/generative-ai/>
</details>

**27.** A retailer is deciding whether to replace its menu-driven support bot with a generative AI assistant. Which TWO are genuine advantages of generative AI for this use case? (Select TWO.)
- A. It can hold natural, multi-turn conversations and understand varied phrasing
- B. It always produces the same response for the same question, which simplifies testing
- C. It never needs guardrails, because foundation models can't produce harmful content
- D. It can generate tailored responses quickly instead of selecting only from fixed scripts
- E. It removes the need to monitor quality, because answers can't drift over time

<details><summary>Answer</summary>

**A, D.** Generative AI offers conversational capability (understanding free-form, multi-turn input) and responsiveness (generating tailored content on the fly), which menu-driven bots can't match.

Why not the others:
- **B.** Generative output is usually nondeterministic, which makes testing harder, not easier.
- **C.** FMs can produce harmful or off-topic content, so guardrails are recommended.
- **E.** Quality should still be monitored. Data, user behavior, and model versions change.

Resource: <https://aws.amazon.com/what-is/generative-ai/>
</details>

**28.** A law firm's assistant cites a court case that sounds real but doesn't exist. What is this failure called?
- A. Overfitting
- B. Hallucination
- C. Tokenization
- D. Underfitting

<details><summary>Answer</summary>

**B.** A hallucination is output that is fluent and confident but factually wrong or invented. It happens because models generate statistically likely text rather than looking up verified facts. Grounding (for example, RAG) and verification reduce the risk.

Why not the others:
- **A.** Overfitting is a training problem in which a model memorizes training data and doesn't generalize.
- **C.** Tokenization is how text is split into tokens. It isn't an error.
- **D.** Underfitting means a model is too simple to learn the data's patterns.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html>
</details>

**29.** A QA engineer runs the same prompt against a text model ten times and gets ten slightly different answers. The product owner asks whether this is a bug. What is the BEST explanation?
- A. It's a bug, because foundation models are deterministic and must always return identical output
- B. The model is being retrained between each call, which changes its answers
- C. Generative models sample from probabilities, so output varies; a lower temperature reduces it
- D. The prompt is too short, and short prompts are the only cause of variation

<details><summary>Answer</summary>

**C.** Text generation picks each next token by sampling from a probability distribution, so results are nondeterministic. Inference parameters such as temperature, top-p, and top-k control how much randomness is used. A lower temperature makes outputs more consistent, but it doesn't guarantee identical results.

Why not the others:
- **A.** Generative models are typically nondeterministic by design.
- **B.** Inference doesn't retrain the model between calls.
- **D.** Variation comes mainly from sampling settings, not from prompt length.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html>
</details>

**30.** A healthcare regulator asks a hospital to explain exactly why its LLM-based triage assistant recommended a particular action for a patient. Why is this request hard to satisfy?
- A. LLMs have billions of parameters, so tracing how an output was produced is very hard
- B. LLMs store each training document as a readable rule that is too long to print
- C. LLMs can only produce explanations in languages the regulator doesn't speak
- D. LLMs delete their internal reasoning after each answer to protect patient privacy

<details><summary>Answer</summary>

**A.** Interpretability is a limitation of large neural networks: their behavior emerges from billions of learned parameters, so they act like black boxes. A model can generate an explanation, but that text isn't a guaranteed account of its internal computation. That's a concern for regulated, high-stakes decisions.

Why not the others:
- **B.** LLMs don't store training documents as readable rules.
- **C.** Language support isn't the issue. The issue is understanding how the model arrived at its output.
- **D.** Models don't have stored reasoning to delete. They have no transparent decision trail to begin with.

Resource: <https://aws.amazon.com/what-is/explainable-ai/>
</details>

**31.** A company's HR assistant tells employees that the parental leave policy is 12 weeks, but the policy was changed to 16 weeks last month. The model was trained before the change. Which approach fixes this limitation MOST directly?
- A. Increase the temperature so the model is more likely to guess a different number
- B. Ask employees to add "please be accurate" to the end of every question
- C. Switch to a larger model, because larger models know about recent policy changes
- D. Retrieve the current policy at request time and include it in the prompt (RAG)

<details><summary>Answer</summary>

**D.** A model's knowledge is frozen at training time and doesn't include private or recent documents. Retrieval Augmented Generation fetches current, authoritative content (such as the updated policy) and adds it to the prompt so the answer is grounded in up-to-date facts.

Why not the others:
- **A.** Higher temperature adds randomness; it doesn't add the missing information.
- **B.** Asking for accuracy can't supply facts the model never learned.
- **C.** A larger model trained on public data still doesn't know the company's private policy update.

Resource: <https://aws.amazon.com/what-is/retrieval-augmented-generation/>
</details>

**32.** A legal team plans to use generative AI to summarize contracts. Which TWO limitations should the team plan to mitigate? (Select TWO.)
- A. The model may hallucinate clauses or terms that aren't in the contract
- B. The model can't process text, so contracts must be converted to images first
- C. The model may give different summaries of the same contract on different runs
- D. The model will refuse to summarize any document longer than one page
- E. The model permanently learns the contracts' confidential terms after each request

<details><summary>Answer</summary>

**A, C.** Hallucination (inventing content) and nondeterminism (varying output) are key limitations for legal use. Grounding, lower temperature, guardrails such as contextual grounding checks, and human review help mitigate them.

Why not the others:
- **B.** Text models process text directly.
- **D.** Context windows of modern models hold far more than a single page, and longer documents can be chunked.
- **E.** Inference doesn't update the model's weights. With Amazon Bedrock, prompts aren't used to train the base models.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html>
</details>

**33.** A company is building a real-time voice assistant for drive-through ordering. Customers hang up if the assistant takes more than a second to answer, and requests are simple ("two coffees, one with oat milk"). Which model selection approach is MOST appropriate?
- A. Choose a smaller, low-latency model that handles the simple task well
- B. Choose the largest, most capable model available, whatever its latency
- C. Choose an image generation model, because the menu includes pictures of each drink
- D. Choose a model only on the size of its context window, which should be as large as possible

<details><summary>Answer</summary>

**A.** Performance requirements drive model selection. For simple, latency-sensitive tasks, a smaller model (such as Amazon Nova Micro or Lite) typically responds faster and costs less while still being accurate enough.

Why not the others:
- **B.** The largest models are usually slower and more expensive, which conflicts with the one-second requirement.
- **C.** Ordering is a language task. Generating images doesn't help.
- **D.** A huge context window isn't needed for short orders and doesn't address latency.

Resource: <https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html>
</details>

**34.** A European bank's compliance team requires that all generative AI inference run in AWS Regions within the EU. The model the developers prefer isn't offered in any EU Region. What should the bank do?
- A. Use the preferred model in a US Region anyway, because inference doesn't count as data processing
- B. Turn off encryption so that the customer data can legally be sent to any AWS Region
- C. Choose a model offered in an EU Region that meets the use case, since compliance limits the choice
- D. Ask the model to promise in its system prompt that it will only ever run in the EU

<details><summary>Answer</summary>

**C.** Compliance and data residency requirements are model selection constraints. The bank should choose a model offered in an approved Region (and check whether cross-Region inference profiles keep traffic within allowed geographies).

Why not the others:
- **A.** Sending prompts containing customer data to a non-approved Region would break the residency requirement.
- **B.** Disabling encryption weakens security and doesn't change where data is processed.
- **D.** A prompt instruction can't control where the model physically runs.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>
</details>

**35.** A marketplace classifies 50 million short product titles a month into one of 30 categories. A large frontier model and a much smaller model both reach the required accuracy on a test set. What should drive the choice?
- A. The larger model, because bigger models are always the better choice in production
- B. The model with the most parameters, because parameter count matters more than cost
- C. The model with the longest maximum output, because classifications need long answers
- D. The smaller model, because it meets the bar at lower cost and latency

<details><summary>Answer</summary>

**D.** When two models meet the quality bar, cost and latency decide. At tens of millions of requests a month, a smaller, simpler model can save a lot of money and respond faster, without any loss in the required quality.

Why not the others:
- **A.** Bigger isn't always better. Extra capability that isn't needed just adds cost and latency.
- **B.** Parameter count is only a rough proxy for capability, and cost matters at this scale.
- **C.** A category label is a few tokens; a long maximum output is irrelevant.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html>
</details>

**36.** A logistics company wants an assistant that reads photos of shipping labels and handwritten delivery notes, then answers drivers' questions about them. Which model capability is the deciding factor?
- A. Support for generating video output
- B. Support for image input (multimodal)
- C. The ability to run without any prompt
- D. The ability to generate music from text

<details><summary>Answer</summary>

**B.** The use case requires the model to understand images, so model selection must start with input modality: only models that accept image input qualify.

Why not the others:
- **A.** The assistant answers questions in text. It doesn't need to produce video.
- **C.** Every foundation model needs input to respond; this isn't a selection factor.
- **D.** Music generation is unrelated to reading labels.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html>
</details>

**37. (Matching)** A team is writing down why it rejected some candidate models. Match each finding to the model selection factor it relates to.
- The model takes four seconds to respond, but the chat feature needs sub-second replies => Latency
- The model would cost three times the project's monthly budget at expected volume => Cost
- The model isn't offered in the Region where regulators require data to stay => Compliance
- The model only accepts text, but the app must analyze product photos => Modality
- The model can't take in the 200-page reports users need to analyze in one request => Context length
Extra choices: Temperature | Fine-tuning

<details><summary>Answer</summary>

Model selection weighs performance requirements such as latency, cost, compliance constraints such as Regions and data residency, capabilities such as input and output modalities, and limits such as the context window. Temperature is an inference parameter and fine-tuning is a customization method; neither is a reason a candidate model fails these requirements.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html>
</details>

**38.** An online clothing store adds a generative AI shopping assistant that answers fit and style questions. Leadership wants to know whether it's helping sales. Which metric measures that MOST directly?
- A. The BLEU score of the assistant's responses against reference answers
- B. The number of tokens in each response
- C. Conversion rate: the share of assistant users who complete a purchase
- D. The model's training loss reported by the vendor

<details><summary>Answer</summary>

**C.** Conversion rate ties the assistant to a business outcome: whether customers who use it buy more often. Comparing users who use the assistant with users who don't (for example, through an A/B test) shows the effect.

Why not the others:
- **A.** BLEU measures overlap with reference text. It says nothing about sales.
- **B.** Token count is a cost and length measure, not a business outcome.
- **D.** Training loss is a technical metric from model training, unrelated to the store's revenue.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html>
</details>

**39.** A music streaming service adds a generative AI feature that creates personalized playlists with written descriptions. Which TWO metrics best show whether the feature increases the business value of each customer? (Select TWO.)
- A. Average revenue per user (ARPU)
- B. Customer lifetime value (CLV)
- C. The number of GPUs in the AWS Region
- D. The ROUGE score of each playlist description
- E. The number of tokens in the system prompt

<details><summary>Answer</summary>

**A, B.** ARPU and customer lifetime value measure how much revenue each customer generates now and over the relationship. If personalized playlists improve engagement and retention, these metrics should rise.

Why not the others:
- **C.** GPU counts in a Region are AWS infrastructure details, not the service's business results.
- **D.** ROUGE measures text overlap with references; it doesn't show revenue or retention.
- **E.** Prompt length is an implementation detail that affects cost, not customer value.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html>
</details>

**40.** A contact center adds a generative AI tool that drafts replies for human agents. Which metric BEST shows an efficiency gain?
- A. A reduction in average handle time per customer case
- B. The number of AWS Regions in which the model is available
- C. An increase in the model's maximum output tokens
- D. The number of parameters in the foundation model

<details><summary>Answer</summary>

**A.** Efficiency metrics measure how much time or effort the solution saves. A drop in average handle time, with satisfaction held steady, shows the drafting tool makes agents more productive.

Why not the others:
- **B.** Regional availability is a deployment detail, not an efficiency outcome.
- **C.** A higher output limit is a configuration setting, not a gain.
- **D.** Parameter count describes the model, not the business impact.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html>
</details>

**41.** A holding company wants to deploy one generative AI assistant across its insurance, retail, and travel businesses instead of buying a separate tool for each. Which business value metric captures whether one model performs well enough across all three?
- A. Inference latency in a single Region
- B. Number of fine-tuning epochs
- C. Size of the embeddings vector
- D. Cross-domain performance

<details><summary>Answer</summary>

**D.** Cross-domain performance measures how well a single model or application handles tasks across different business domains. Strong cross-domain performance is what makes a shared solution worth more than several specialized ones.

Why not the others:
- **A.** Latency in one Region says nothing about quality across business domains.
- **B.** Fine-tuning epochs are a training setting, not a business value measure.
- **C.** Embedding dimensions are a technical detail of the model.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html>
</details>

**42.** A CFO asks for evidence that a generative AI document-processing project was worth its cost. Which TWO measures support a return on investment (ROI) case? (Select TWO.)
- A. Labor hours saved per month, valued at the cost of those hours
- B. The temperature setting used by the model in production
- C. Total cost of the solution, including usage, development, and upkeep
- D. The number of transformer layers and attention heads in the model
- E. The length of the system prompt, measured in characters per request

<details><summary>Answer</summary>

**A, C.** ROI compares the benefit delivered (for example, the value of labor hours saved or revenue gained) with the total cost of building and running the solution.

Why not the others:
- **B.** Temperature is a configuration setting, not a measure of value.
- **D.** The number of layers describes the model architecture, not business value.
- **E.** Prompt length affects cost per request but isn't by itself an ROI measure.

Resource: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html>
</details>

## Task 2.3: Describe AWS infrastructure and technologies for building GenAI applications

**43.** A startup wants to try foundation models from several providers — such as Amazon, Anthropic, Meta, and Mistral AI — through one API, with no infrastructure to manage, and switch models easily as it experiments. Which AWS service should it use?
- A. Amazon EC2 with a different self-managed server for each model provider
- B. Amazon Bedrock, which offers many FMs through a single serverless API
- C. Amazon Personalize, which recommends the best model for each request
- D. AWS Glue, which converts data into the format each model provider needs

<details><summary>Answer</summary>

**B.** Amazon Bedrock is a fully managed, serverless service that provides access to foundation models from Amazon and leading AI companies through a unified API, along with tools for customization, RAG, agents, guardrails, and evaluation.

Why not the others:
- **A.** Self-managed servers add operational work, and many proprietary models can't be self-hosted at all.
- **C.** Personalize builds recommendation systems for users and items, not model routing.
- **D.** Glue is a data integration and ETL service. It doesn't host or serve FMs.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>
</details>

**44.** A data science team wants to train its own model architecture from scratch on proprietary data, choose the exact GPU instances, and control the full training and hosting process. Which AWS service is designed for this?
- A. Amazon SageMaker AI, which provides managed infrastructure and tools to build, train, and deploy models
- B. Amazon Bedrock, which only offers pre-trained models through an API and never allows any customization
- C. Amazon Comprehend, which lets teams upload any neural network architecture for training
- D. Amazon Quick, which trains custom deep learning architectures from dashboards

<details><summary>Answer</summary>

**A.** SageMaker AI gives data scientists full control over building, training (including distributed training on chosen instances), tuning, and deploying their own models, with managed infrastructure.

Why not the others:
- **B.** Bedrock does support customization such as fine-tuning, but it isn't the service for training a custom architecture from scratch on chosen instances.
- **C.** Comprehend offers managed NLP and custom classification, not arbitrary architectures.
- **D.** Quick is for business users' analytics, research, and automation, not model training.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html>
</details>

**45.** A data scientist wants to deploy a popular open-weight LLM into the company's own SageMaker AI environment and fine-tune it on internal data, starting from a ready-made template rather than writing deployment code. Which feature should they use?
- A. AWS Glue Data Catalog
- B. Amazon SageMaker JumpStart
- C. Amazon SageMaker Ground Truth
- D. AWS Trusted Advisor

<details><summary>Answer</summary>

**B.** SageMaker JumpStart is an ML hub with pre-trained models, including many open-weight foundation models, that can be deployed and fine-tuned in a SageMaker AI environment with a few clicks or a few lines of code.

Why not the others:
- **A.** The Glue Data Catalog stores metadata about datasets; it doesn't deploy or fine-tune models.
- **C.** Ground Truth creates labeled datasets; it doesn't provide pre-trained models to deploy.
- **D.** Trusted Advisor checks accounts against best practices for cost, security, and more.

Resource: <https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html>
</details>

**46.** A developer wants to build an AI agent in Python by writing only a prompt and a list of tools, and let the model plan and choose tools itself, using an open-source SDK that works with Amazon Bedrock and other model providers. Which AWS offering fits?
- A. Amazon Lex V2 intents and slots
- B. Amazon SageMaker Ground Truth
- C. Strands Agents
- D. AWS Glue DataBrew

<details><summary>Answer</summary>

**C.** Strands Agents is an open-source SDK (Python and TypeScript) for building agents with a model-driven approach: the developer supplies a model, a prompt, and tools, and the model's reasoning drives the agent loop. It supports MCP tools, multi-agent patterns, and many model providers, and deploys to services such as Amazon Bedrock AgentCore.

Why not the others:
- **A.** Lex builds intent-based chatbots with predefined dialog flows, not model-driven agents.
- **B.** Ground Truth is a data labeling service.
- **D.** DataBrew is a visual data preparation tool.

Resource: <https://strandsagents.com/latest/>
</details>

**47.** A company has built agents with several open-source frameworks. It now needs a secure, serverless place to run them at scale with session isolation, built-in identity, and observability, without managing infrastructure. Which AWS service is purpose-built for this?
- A. Amazon Translate, which converts each framework's code into one language
- B. Amazon S3 Glacier, which stores agents so that they run only when restored
- C. Amazon Rekognition, which watches agents' screens for problems
- D. Amazon Bedrock AgentCore, using AgentCore Runtime with its other services

<details><summary>Answer</summary>

**D.** Amazon Bedrock AgentCore is an agentic platform for running and operating agents securely at scale with any framework and any model. AgentCore Runtime provides serverless hosting with session isolation, and other modular services (Memory, Gateway, Identity, Policy, Observability, Evaluations, Code Interpreter, Browser) add what production agents need.

```arch
users: users Users
cloud AWS Cloud
  rt: agentcore *AgentCore Runtime | any framework
  col [col]
    id: agentcore Identity
    mem: agentcore Memory
    gw: agentcore Gateway | MCP tools
    obs: cloudwatch Observability
  fm: bedrock Foundation model
---
users -> rt : invoke agent
rt -> id
rt -> mem
rt -> gw
rt ~> obs : traces
rt -> fm
```

Why not the others:
- **A.** Translate converts natural-language text, not code, and doesn't host agents.
- **B.** Glacier is archival storage. It doesn't run anything.
- **C.** Rekognition analyzes images and video; it isn't an agent runtime.

Resource: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html>
</details>

**48.** A company wants its agents to use dozens of existing internal REST APIs and AWS Lambda functions as tools. It wants to expose them through a managed MCP-compatible endpoint rather than rewriting each one as an MCP server. Which service fits?
- A. Amazon CloudFront
- B. AWS Trusted Advisor
- C. Amazon SageMaker Feature Store
- D. Amazon Bedrock AgentCore Gateway

<details><summary>Answer</summary>

**D.** AgentCore Gateway converts APIs, Lambda functions, and existing services into MCP-compatible tools and can connect to existing MCP servers, making them available to agents through a single, secured gateway endpoint.

```arch
row
  agent: agentcore Agent
  gw: agentcore *AgentCore Gateway | MCP endpoint
  col [col]
    api: apigw REST APIs
    fn: lambda Lambda functions
    mcp: server MCP servers
---
agent -> gw : MCP
gw -> api
gw -> fn
gw -> mcp
```

Why not the others:
- **A.** CloudFront is a content delivery network. It doesn't turn APIs into agent tools.
- **B.** Trusted Advisor gives account best-practice recommendations.
- **C.** Feature Store stores ML features for training and inference.

Resource: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html>
</details>

**49. (Matching)** A cloud center of excellence is publishing a one-page guide to AWS generative AI offerings. Match each offering to its main purpose.
- Serverless API access to foundation models from many providers => Amazon Bedrock
- Building, training, and deploying custom ML models with full control => Amazon SageMaker AI
- A hub of pre-trained models to deploy and fine-tune in your own environment => SageMaker JumpStart
- AI agents, research, automation, and BI for business users => Amazon Quick
- An agentic IDE for spec-driven software development => Kiro
- An open-source SDK for building model-driven agents in code => Strands Agents
- Running and governing agents securely at scale with any framework => Amazon Bedrock AgentCore

<details><summary>Answer</summary>

Bedrock is the managed FM API platform. SageMaker AI is the full ML platform. JumpStart is SageMaker AI's model hub. Quick serves business users with agents and analytics. Kiro helps developers build software with AI. Strands Agents is a framework for writing agents. AgentCore runs and operates agents in production.

Resource: <https://aws.amazon.com/ai/generative-ai/>
</details>

**50.** A mid-sized insurer with a small IT team wants to launch a claims-summary feature within one quarter. Why do managed AWS generative AI services such as Amazon Bedrock suit this goal?
- A. They require the insurer to pre-train its own foundation model first, which guarantees quality
- B. They only work after the insurer hires a large team of ML researchers
- C. They lower the barrier to entry and speed time to market, because no model hosting or training is needed
- D. They remove all security responsibilities from the insurer under the shared responsibility model

<details><summary>Answer</summary>

**C.** Managed services provide ready-to-use FMs through an API, with built-in tools for RAG, guardrails, and evaluation. That makes generative AI accessible to small teams and lets them deliver business value quickly without managing infrastructure.

Why not the others:
- **A.** Pre-training a model is exactly the expensive, slow work managed services remove.
- **B.** Managed services are designed for developers without deep ML expertise.
- **D.** Customers stay responsible for security in the cloud, such as IAM, data, and application controls.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>
</details>

**51.** A startup compares building its own GPU cluster to host open-source models with using Amazon Bedrock. Which TWO are advantages of the managed AWS service? (Select TWO.)
- A. Pay-as-you-go pricing without buying or reserving hardware up front
- B. Guaranteed hallucination-free responses for every model in the catalog
- C. No servers to provision, patch, or scale for model hosting
- D. Automatic legal ownership of all content that any model generates
- E. Exemption from the need to evaluate models before production use

<details><summary>Answer</summary>

**A, C.** Managed generative AI services are cost-effective for variable usage (pay per use) and efficient to operate (no infrastructure management), which speeds delivery.

Why not the others:
- **B.** No model is hallucination-free. Grounding and evaluation are still needed.
- **D.** Using a managed service doesn't settle intellectual property questions about generated content.
- **E.** Models should always be evaluated for the specific use case.

Resource: <https://aws.amazon.com/bedrock/pricing/>
</details>

**52.** A healthcare company's security officer asks how Amazon Bedrock treats the prompts and responses the company sends. Which statement is accurate?
- A. Bedrock shares all prompts with model providers so that they can improve their public models
- B. Bedrock doesn't use customer prompts or outputs to train base models or share them with providers
- C. Bedrock stores every prompt in a public dataset that researchers can download
- D. Bedrock requires customers to disable encryption so that the models can read their data

<details><summary>Answer</summary>

**B.** Amazon Bedrock doesn't store or use customers' prompts and completions to train AWS models and doesn't distribute them to third parties. Model providers don't have access to customer data. Data is encrypted in transit and at rest, and customers can use their own KMS keys and private connectivity through AWS PrivateLink.

```arch
cloud AWS Cloud
  vpc Company VPC
    app: ec2 Clinical app
    ep: privatelink VPC endpoint | PrivateLink
  br: bedrock *Amazon Bedrock
  kms: kms AWS KMS | customer managed key
  prov: users Model providers
---
app -> ep
ep -> br : encrypted in transit
br ~> kms : encrypt at rest
br -x-> prov : no access to customer data
```

Why not the others:
- **A.** Providers don't receive customer prompts or outputs.
- **C.** Customer content isn't published or used as a research dataset.
- **D.** Encryption is on by default and isn't something customers must disable.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html>
</details>

**53.** Under the AWS shared responsibility model, which task is the customer's responsibility when building an application on Amazon Bedrock?
- A. Configuring IAM permissions and protecting the data the application sends to models
- B. Maintaining the physical security of the data centers where Bedrock runs
- C. Patching the operating systems of the servers that host the foundation models
- D. Replacing failed GPUs in the Bedrock fleet

<details><summary>Answer</summary>

**A.** AWS is responsible for security of the cloud: facilities, hardware, and the managed service infrastructure. Customers are responsible for security in the cloud: who can call which models (IAM), what data they send, encryption choices, guardrails, and application-level controls.

Why not the others:
- **B.** Physical data center security is AWS's responsibility.
- **C.** Patching the underlying hosts of a managed service is handled by AWS.
- **D.** Hardware maintenance is AWS's responsibility.

Resource: <https://aws.amazon.com/compliance/shared-responsibility-model/>
</details>

**54.** A company's generative AI feature on Amazon Bedrock serves a large, steady volume of requests around the clock and is sometimes throttled at peak times. It wants a guaranteed level of throughput for a specific model. Which option should it consider?
- A. Lowering the temperature, which makes requests process faster during peaks
- B. Provisioned Throughput, which reserves model units for a committed throughput
- C. Switching all real-time user requests to batch inference jobs instead
- D. Moving request data to Amazon S3 Glacier to reduce the number of requests

<details><summary>Answer</summary>

**B.** Provisioned Throughput lets customers buy model units that guarantee a level of throughput for a model, billed hourly for a term. It suits steady, high-volume workloads that need consistent capacity; for spiky or low volume, on-demand pricing is usually cheaper.

Why not the others:
- **A.** Temperature controls randomness, not capacity.
- **C.** Batch inference processes jobs asynchronously, which doesn't suit interactive users who need immediate answers.
- **D.** Glacier is archival storage and has nothing to do with model capacity.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html>
</details>

**55.** Every weekend, a publisher generates summaries for 2 million archived articles. Results are needed by Monday morning, not in real time. Which Amazon Bedrock option reduces cost the MOST for this job?
- A. On-demand inference with the Priority service tier selected for every request
- B. Provisioned Throughput purchased for a six-month term to cover the weekend job
- C. Sending each request three times to make sure that at least one of them succeeds
- D. Batch inference, which processes prompts asynchronously at a lower price than on-demand

<details><summary>Answer</summary>

**D.** Bedrock batch inference runs a file of prompts stored in S3 asynchronously and writes results back to S3, at a significantly lower price than on-demand inference for supported models. It suits large, non-urgent jobs.

Why not the others:
- **A.** Priority tier costs more in exchange for the fastest responses, which this job doesn't need.
- **B.** A long Provisioned Throughput commitment would be billed all week for a weekend-only job.
- **C.** Duplicating requests multiplies the cost.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html>
</details>

**56.** A company runs two on-demand workloads on Amazon Bedrock: a customer-facing chat that needs the fastest possible responses, and internal document tagging that can wait longer if that saves money. Which service tiers fit each workload?
- A. Flex tier for the chat; Priority tier for the document tagging
- B. Standard tier for both, because service tiers only change the Region used
- C. Priority tier for the chat; Flex tier for the document tagging
- D. Reserved tier for the document tagging; batch inference for the chat

<details><summary>Answer</summary>

**C.** Bedrock service tiers trade cost against performance. Priority tier processes requests ahead of others for a price premium, which suits latency-sensitive, customer-facing traffic. Flex tier offers a discount for workloads that can tolerate longer processing times.

Why not the others:
- **A.** This swaps the tiers: Flex would slow the chat, and Priority would overpay for background tagging.
- **B.** Service tiers change request prioritization and price, not the Region.
- **D.** Reserving capacity for a latency-tolerant background job wastes money, and batch inference is asynchronous, so it can't serve live chat.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html>
</details>

**57.** A global app on Amazon Bedrock is throttled during traffic spikes in its home Region. Engineers propose cross-Region inference. What trade-off should the compliance team review?
- A. Requests may run in other Regions in the profile's geography, affecting residency
- B. Cross-Region inference turns off encryption for any requests routed to other Regions
- C. Cross-Region inference requires retraining the model in every Region that it uses
- D. Cross-Region inference only works for image generation models, not for text models

<details><summary>Answer</summary>

**A.** Cross-Region inference improves availability and throughput by routing requests to other Regions defined in an inference profile (for example, a US or EU geography). Data in transit stays encrypted, but processing may occur outside the source Region, so residency requirements must be checked.

Why not the others:
- **B.** Traffic remains encrypted. The question is where it's processed.
- **C.** It routes requests to the same model offered in other Regions. No retraining happens.
- **D.** Cross-Region inference supports many text models.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>
</details>

**58.** A chatbot sends the same 4,000-token product catalog and instructions at the start of every request, followed by a short user question. Which TWO actions would lower its cost on Amazon Bedrock? (Select TWO.)
- A. Use prompt caching so that the repeated prefix is cached and billed at a reduced rate
- B. Raise the maximum output tokens so the model can give longer answers
- C. Use a smaller, cheaper model if it still meets the accuracy requirement
- D. Duplicate the catalog in the prompt so the model reads it twice
- E. Use the Priority service tier for every request

<details><summary>Answer</summary>

**A, C.** Prompt caching stores a repeated prompt prefix so later requests read it from the cache at a reduced token price and with lower latency. A smaller model that meets requirements lowers the per-token price.

Why not the others:
- **B.** Longer answers mean more output tokens and higher cost.
- **D.** Duplicating content doubles the input tokens.
- **E.** Priority tier carries a price premium.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html>
</details>

**59.** A new internal assistant will have unpredictable usage: a few hundred requests on some days and almost none on others. Which pricing approach is MOST cost-effective?
- A. Provisioned Throughput with a long-term commitment
- B. On-demand, pay-per-token inference
- C. Reserved tier capacity for the maximum expected load
- D. Buying dedicated GPU instances that run all the time

<details><summary>Answer</summary>

**B.** With low and unpredictable traffic, on-demand pricing charges only for the tokens actually processed, with no idle capacity to pay for.

Why not the others:
- **A.** Provisioned Throughput bills for reserved capacity whether or not it's used.
- **C.** Reserved tier is also billed for committed capacity, which suits mission-critical, steady workloads.
- **D.** Always-on instances pay for idle time on quiet days.

Resource: <https://aws.amazon.com/bedrock/pricing/>
</details>

**60.** A team is debating whether to fine-tune a foundation model or improve its prompts. Which statement about the cost trade-off is accurate?
- A. Fine-tuning is free, because the provider pays for the compute used to train the custom model
- B. Prompt engineering always costs more than fine-tuning because prompts are billed per character
- C. Fine-tuning adds training and data preparation costs, and hosting a custom model can add ongoing costs
- D. Fine-tuned models never need evaluation, so they reduce total cost of ownership

<details><summary>Answer</summary>

**C.** Customizing a model costs extra: preparing labeled data, running training jobs (billed by tokens processed or by compute), storing the custom model, and in many cases paying for dedicated capacity to run it. Prompt engineering and RAG are usually cheaper to try first.

Why not the others:
- **A.** Customers pay for model customization jobs.
- **B.** Prompt engineering is generally the cheapest way to adapt a model; billing is by tokens, not characters.
- **D.** Fine-tuned models still need evaluation before and after deployment.

Resource: <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>
</details>
