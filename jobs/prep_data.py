# MCQ Interview Prep Questions

MCQ_QUESTIONS = {
    'it': [
        {
            'id': 1,
            'question': "What is the primary purpose of Django's Middleware?",
            'choices': [
                "To define the database schema and model relationships",
                "To process requests and responses globally before they reach the view or after they leave it",
                "To compile static assets like CSS and JavaScript files",
                "To handle database connection pooling automatically"
            ],
            'correct_index': 1,
            'explanation': "Django Middleware is a framework of hooks that run globally during request and response processing. It is commonly used for sessions, authentication, and security headers."
        },
        {
            'id': 2,
            'question': "In Python, what is the difference between list.append() and list.extend()?",
            'choices': [
                "append() adds a single element; extend() adds elements of an iterable individually",
                "append() creates a new list; extend() modifies the list in place",
                "append() can only add strings; extend() can add any object type",
                "There is no difference; they are aliases for the same function"
            ],
            'correct_index': 0,
            'explanation': "append() adds its argument as a single element to the end of a list. extend() iterates over its argument, adding each item to the list, thus expanding it."
        },
        {
            'id': 3,
            'question': "Which database normalization form ensures that all non-key attributes are fully functionally dependent on the primary key (no partial dependencies)?",
            'choices': [
                "First Normal Form (1NF)",
                "Second Normal Form (2NF)",
                "Third Normal Form (3NF)",
                "Boyce-Codd Normal Form (BCNF)"
            ],
            'correct_index': 1,
            'explanation': "Second Normal Form (2NF) requires that the table is in 1NF and all non-key columns must depend on the entire primary key, eliminating partial dependencies."
        },
        {
            'id': 4,
            'question': "What is the complexity of searching for an element in a balanced Binary Search Tree (BST)?",
            'choices': [
                "O(1)",
                "O(N)",
                "O(log N)",
                "O(N log N)"
            ],
            'correct_index': 2,
            'explanation': "In a balanced BST, each step divides the search space in half, resulting in a logarithmic time complexity of O(log N)."
        },
        {
            'id': 5,
            'question': "What does the 'git merge' command do?",
            'choices': [
                "Deletes a branch from the repository",
                "Integrates changes from one branch into another active branch",
                "Pushes changes directly to the remote repository",
                "Reverts the codebase to a previous stable commit state"
            ],
            'correct_index': 1,
            'explanation': "git merge combines the work of multiple branches together, integrating the commit history of a source branch into the current target branch."
        }
    ],
    'finance': [
        {
            'id': 1,
            'question': "Which financial statement provides a snapshot of a company's assets, liabilities, and equity at a specific point in time?",
            'choices': [
                "Income Statement",
                "Balance Sheet",
                "Cash Flow Statement",
                "Statement of Retained Earnings"
            ],
            'correct_index': 1,
            'explanation': "The Balance Sheet summarizes a company's financial position at a single point in time, showing the basic accounting equation: Assets = Liabilities + Shareholders' Equity."
        },
        {
            'id': 2,
            'question': "What does EBITDA stand for?",
            'choices': [
                "Earnings Before Interest, Taxes, Depreciation, and Amortization",
                "Equity Balance In Total Debt Assets",
                "Estimated Business Income Taxes, Debt, and Audit",
                "Earnings Before Inflation, Tariffs, Deficits, and Accounts"
            ],
            'correct_index': 0,
            'explanation': "EBITDA is a widely used financial metric that measures overall operational performance, computed as Earnings Before Interest, Taxes, Depreciation, and Amortization."
        },
        {
            'id': 3,
            'question': "Under the capital asset pricing model (CAPM), what does Beta measure?",
            'choices': [
                "The total risk of an individual stock including company-specific factors",
                "The volatility/systematic risk of a security in comparison to the market as a whole",
                "The rate of return on a risk-free government bond",
                "The ratio of net income to shareholder equity"
            ],
            'correct_index': 1,
            'explanation': "Beta measures systematic risk—the volatility of a stock relative to the broader market. A Beta of 1 matches the market; >1 means higher volatility; <1 means lower volatility."
        },
        {
            'id': 4,
            'question': "What is the key difference between Debt and Equity financing?",
            'choices': [
                "Debt financing gives away company ownership; Equity financing does not",
                "Debt financing must be repaid with interest; Equity financing gives ownership shares with no repayment obligation",
                "Equity financing is only available for government agencies",
                "Debt financing carries no risk of bankruptcy"
            ],
            'correct_index': 1,
            'explanation': "Debt financing involves borrowing funds that must be repaid over time with interest. Equity financing raises money by selling ownership shares (stock) to investors."
        },
        {
            'id': 5,
            'question': "In accounting, what is the 'matching principle'?",
            'choices': [
                "Matching assets and liabilities perfectly to equal zero",
                "Recognizing expenses in the same period as the revenues they helped generate",
                "Matching tax filings with federal audit reports annually",
                "Ensuring that cash inflow matches cash outflow in each department"
            ],
            'correct_index': 1,
            'explanation': "The matching principle requires that expenses be reported in the same period as the revenues they helped earn, ensuring accurate calculation of net profit."
        }
    ],
    'marketing': [
        {
            'id': 1,
            'question': "In digital marketing, what does SEO stand for?",
            'choices': [
                "Sales Execution Optimization",
                "Search Engine Optimization",
                "Social Engagement Outlet",
                "Structured Email Operations"
            ],
            'correct_index': 1,
            'explanation': "SEO stands for Search Engine Optimization. It is the process of improving organic site traffic and ranking positions on search engines like Google."
        },
        {
            'id': 2,
            'question': "What is 'Click-Through Rate' (CTR) in online advertising?",
            'choices': [
                "The percentage of users who clicked an ad out of total users who saw it",
                "The cost paid for each click received on an advertising link",
                "The number of times an ad is served to a unique browser user",
                "The percentage of clicks that converted into actual product sales"
            ],
            'correct_index': 0,
            'explanation': "CTR is calculated as (Clicks / Impressions) * 100. It measures how attractive or relevant an ad is to the viewing audience."
        },
        {
            'id': 3,
            'question': "Which model outlines the stages a consumer goes through before making a purchase?",
            'choices': [
                "The SWOT Model",
                "The AIDA Model (Attention, Interest, Desire, Action)",
                "The BCG Matrix",
                "The Ansoff Product Market Grid"
            ],
            'correct_index': 1,
            'explanation': "The AIDA model describes the cognitive stages of consumer buying: first capturing Attention, building Interest, creating Desire, and prompting Action."
        },
        {
            'id': 4,
            'question': "What is the primary difference between Push and Pull marketing?",
            'choices': [
                "Push marketing is cheaper than Pull marketing",
                "Push marketing actively takes products to the customer; Pull marketing draws customers naturally to the brand",
                "Push marketing is online; Pull marketing is print/traditional only",
                "Push marketing uses AI; Pull marketing is manual"
            ],
            'correct_index': 1,
            'explanation': "Push marketing 'pushes' promotional content directly to target audiences (e.g. direct ads). Pull marketing 'pulls' interested consumers in (e.g. blog posts, SEO, content marketing)."
        },
        {
            'id': 5,
            'question': "What is A/B testing in conversion optimization?",
            'choices': [
                "Testing a brand logo with two different target colors",
                "Comparing two versions of a webpage (A and B) with one variable changed to see which performs better",
                "Surveys sent to Group A and Group B candidates to collect demographic info",
                "Automated software scanning for spelling errors in advertising copy"
            ],
            'correct_index': 1,
            'explanation': "A/B testing is a controlled experiment where two variants (A and B) are shown to users at random to measure statistical differences in conversions or user responses."
        }
    ],
    'hr': [
        {
            'id': 1,
            'question': "What is the primary objective of a structured onboarding process?",
            'choices': [
                "To test the employee's technical capabilities one final time",
                "To integrate new hires smoothly into the company culture, clarify expectations, and accelerate productivity",
                "To explain the legal terms of firing policies in detail",
                "To handle the background check verification documentation"
            ],
            'correct_index': 1,
            'explanation': "Onboarding helps new hires assimilate into their roles, understand cultural values, clarify tasks, and feel welcomed, which improves retention and time-to-productivity."
        },
        {
            'id': 2,
            'question': "Which interview method asks candidates to describe past behaviors in specific situations to predict future performance?",
            'choices': [
                "Stress Interviewing",
                "Behavioral Event Interviewing (STAR method)",
                "Unstructured Screening",
                "Technical Coding Assessments"
            ],
            'correct_index': 1,
            'explanation': "Behavioral interviewing uses the STAR method (Situation, Task, Action, Result) to evaluate how candidates handled specific situations in the past as an indicator of future performance."
        },
        {
            'id': 3,
            'question': "What is the term for the departure of employees from an organization (e.g. through resignation or retirement) over time?",
            'choices': [
                "Attrition",
                "Sourcing",
                "Onboarding",
                "Acquisition"
            ],
            'correct_index': 0,
            'explanation': "Attrition refers to the natural reduction of a workforce as employees leave due to resignation, retirement, or transfer, and are not immediately replaced."
        },
        {
            'id': 4,
            'question': "What does the 'STAR' framework in behavioral interview answers stand for?",
            'choices': [
                "Skills, Tasks, Answers, Recommendations",
                "Situation, Task, Action, Result",
                "Standard Training And Recruitment",
                "Strategy, Timeline, Assessment, Review"
            ],
            'correct_index': 1,
            'explanation': "STAR stands for Situation, Task, Action, and Result. It is the recommended structure for answering behavioral interview questions."
        },
        {
            'id': 5,
            'question': "In compensation, what is 'Equity' referring to?",
            'choices': [
                "Providing company stock options or ownership shares as part of the compensation package",
                "Providing equivalent paid time off policies to all employees",
                "Ensuring all employees receive the exact same monthly base pay",
                "Providing health insurance plans with zero premiums"
            ],
            'correct_index': 0,
            'explanation': "Equity compensation gives employees a stake in the business's growth (e.g. stock options, RSUs), aligning their financial incentives with the long-term success of the company."
        }
    ]
}
