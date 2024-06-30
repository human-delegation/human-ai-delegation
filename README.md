The research data in this repository are a snapshot of the data that were used in the research paper.

The repository includes a data folder named "ResearchData". The folder contains 875 files, each represents the data for a single retail store. The file name follows the format: store_id_<ID>_<Owner Type>.csv. 
<ID> is the censored store ID.
<Owner Type> is the type of store managers, with "F" indicating franchise managers and "S" indicating stores owned by the company.

Each file contains the following columns:

1. period: number of weeks since the AI was introduced to this store.
2. DelegationDecision: percentage of tasks delegated to AI.
3. sale_improvement	: Team vs. Human, the manager's sales improvement in period t after AI implementation.
4. Manager_outperform: Team vs. AI, sales performance comparison between order by pure system and order after the manager's modification'' in period t	
5.  outperform_area: Team vs. Team, difference of sales improvement between the retail store and the regional average after AI implementation in period t
6. BadWeather: Number of days with bad weather (rainy, snowy, etc.) in period t.
7. Holiday: Number of holidays in period t.

The rest columns are calculated for alternative measurements of DV and for different categories of items.

8. dele_demand: percentage of tasks delegated to AI at the product-quantity level.
9. dele_item_bakery: percentage of tasks for bakery products delegated to AI.
10. dele_item_dairy: percentage of tasks for dairy products delegated to AI.
11. sale_bakery_improvement: Team vs. Human, the manager's sales improvement in period t after AI implementation for bakery products.
12. sale_dairy_improvement: Team vs. Human, the manager's sales improvement in period t after AI implementation for dairy products.
13. Manager_outperform_bakery: Team vs. AI, sales performance comparison between order by pure system and order after the manager's modification'' in period t for bakery products.
14. Manager_outperform_dairy: eam vs. AI, sales performance comparison between order by pure system' and order after the manager's modification in period t for dairy products.
15. outperform_area_bakery: Team vs. Team, difference of sales improvement between the retail store and the regional average after AI implementation in period t for bakery products.
16. outperform_area_dairy: Team vs. Team, difference of sales improvement between the retail store and the regional average after AI implementation in period t for dairy products.