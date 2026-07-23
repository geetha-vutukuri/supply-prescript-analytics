# supply-prescript-analytics

🚀 Exciting Update: Kickstarting my Internship at Alxero Solutions!

I am thrilled to share that I have officially started my internship journey with the team at Alxero Solutions! For my primary project, I will be building SupplyPrescript—a Closed-Loop Prescriptive Analytics platform tailored for Supply Chain Operations & Operations Research. 📦🤖

Most modern dashboards tell you what happened or predict what will happen, but they stop short of telling the operator what to do. SupplyPrescript bridges this gap by combining machine learning with mathematical optimization to suggest optimal operational alternatives (like air freight vs. secondary sourcing) when disruptions hit, while continuously learning from the real-world outcomes of human decisions.

🎯 Week 1 Milestones Achieved:

Data Engineering: Developed a synthetic operational dataset mimicking supplier reliability metrics, distances, and real-world bottleneck factors.

Predictive Baseline: Built and optimized an XGBoost Regressor prototype to forecast precise shipping delays in days.

Data Architecture: Fully mapped out and initialized a relational transactional database schema (shipments, prescriptions, and executed_decisions) to anchor our write-back pipeline.



📦 Week 2: Mathematical Optimization & Prescriptive Analytics

This notebook extends the delay prediction system by adding a prescriptive analytics layer using Mathematical Optimization (Linear Programming).

🎯 Objective

When a delay is predicted, the system should:

Evaluate multiple corrective actions
Optimize decision-making under constraints
Recommend the best strategies based on Cost vs Speed trade-offs
🧠 Approach
1. Business Constraints Defined

The model incorporates real-world constraints such as:

Budget limitations 💰
Maximum allowable delay reduction ⏱️
Feasible action combinations
2. Optimization Model

We use Linear Programming (SciPy) to:

Minimize total cost OR delay impact
Generate multiple strategies:
Low Cost Strategy
Fast Delivery Strategy
Balanced Strategy
3. Decision Variables

Each possible action is treated as a binary variable:

Expedite shipping 🚚
Use backup supplier 🏭
Increase inventory 📦
4. Output (Prescriptive Recommendations)

For each strategy, the system provides:

Selected actions ✅
Total cost 💰
Time impact ⏱️
Trade-off explanation ⚖️

🔄 Workflow
Predict delay (Week 1 model)
Trigger optimization if delay detected
Generate best alternative strategies
Display actionable insights
🚀 Key Highlights

✔️ Combines Predictive + Prescriptive Analytics
✔️ Real-world business decision modeling
✔️ Multi-strategy optimization
✔️ Clear trade-off visualization

📌 Conclusion

This module demonstrates how optimization techniques can be used to:

Improve operational efficiency
Reduce delays
Support intelligent decision-making in supply chain/logistics systems
