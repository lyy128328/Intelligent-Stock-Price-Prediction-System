#%matplotlib inline
import daft
import pymc
import matplotlib.pyplot as plt
import matplotlib as mlp
import numpy as np
import ggplot
import pandas as pd

# Initialization
observed_values = [1.]

# Tier 1 node
new_product_release = pymc.Bernoulli('new_product_release', 0.197933, value=np.ones(len(observed_values)))

negative_news = pymc.Bernoulli('negative_news', 0.0389507, value=np.ones(len(observed_values)))

S_and_P_500 = pymc.Bernoulli('S_and_P_500', 0.534976, value=np.ones(len(observed_values)))

Nasdaq = pymc.Bernoulli('Nasdaq', 0.547695, value=np.ones(len(observed_values)))

# Tier 2 node
p_sales = pymc.Lambda('p_sales', lambda new_product_release=new_product_release, negative_news=negative_news: \
                      np.where(new_product_release, np.where(negative_news, 1-10e-5, 0.628571), \
                                                    np.where(negative_news, 0.1, 0.414414)))

sales = pymc.Bernoulli('sales', p_sales, value=np.ones(len(observed_values)))

# Tier 3 node
p_month_average_price = pymc.Lambda('p_month_average_price', lambda sales=sales, new_product_release=new_product_release: \
                                   np.where(sales, np.where(new_product_release, 0.660819, 0.498795), \
                                           np.where(new_product_release, 0.551282, 0.429293)))

month_average_price = pymc.Bernoulli('month_average_price', p_month_average_price, value=np.ones(len(observed_values)))

p_month_average_volumn = pymc.Lambda('p_month_average_volumn', lambda sales=sales, new_product_release=new_product_release:\
                                   np.where(sales, np.where(new_product_release, 0.438596, 0.448193), \
                                           np.where(new_product_release, 0.769231, 0.358586)))

month_average_volumn = pymc.Bernoulli('month_average_volumn', p_month_average_volumn, value=np.ones(len(observed_values)))

# Tier 4 node
p_yesterday_price_change = pymc.Lambda('p_yesterday_price_change', lambda month_average_price=month_average_price, \
                                      month_average_volumn=month_average_volumn, S_and_P_500=S_and_P_500, Nasdaq=Nasdaq: \
                                      np.where(month_average_price, \
                                               np.where(month_average_volumn, \
                                                        np.where(S_and_P_500, \
                                                                 np.where(Nasdaq, 0.695652, 0.125), \
                                                                 np.where(Nasdaq, 0.647059, 0.290323)), \
                                                        np.where(S_and_P_500, \
                                                                 np.where(Nasdaq, 0.711628, 0.428571), \
                                                                 np.where(Nasdaq, 0.589744, 0.27933))), \
                                               np.where(month_average_volumn, \
                                                        np.where(S_and_P_500, \
                                                                 np.where(Nasdaq, 0.724719, 0.304348), \
                                                                 np.where(Nasdaq, 0.529412, 0.342105)), \
                                                        np.where(S_and_P_500, \
                                                                 np.where(Nasdaq, 0.689394, 0.210526), \
                                                                 np.where(Nasdaq, 0.5, 0.268041)))))

yesterday_price_change = pymc.Bernoulli('yesterday_price_change', p_yesterday_price_change, value=np.ones(len(observed_values)))

p_yesterday_price_volumn = pymc.Lambda('p_yesterday_price_volumn', lambda \
                                       p_month_average_price=p_month_average_price, month_average_volumn=month_average_volumn: \
                                       np.where(p_month_average_price, np.where(month_average_volumn, 0.469512, 0.475771), \
                                                                       np.where(month_average_volumn, 0.489189, 0.448148)))

yesterday_price_volumn = pymc.Bernoulli('yesterday_price_volumn', p_yesterday_price_volumn,  value=np.ones(len(observed_values)))

# Tier 5 node
p_today_price_change = pymc.Lambda('p_today_price_change', lambda month_average_price=month_average_price,\
                                   month_average_volumn=month_average_volumn, yesterday_price_change=yesterday_price_change, \
                                   yesterday_price_volumn=yesterday_price_volumn:\
                                   np.where(month_average_price, \
                                            np.where(month_average_volumn, \
                                                     np.where(yesterday_price_change, \
                                                             np.where(yesterday_price_volumn, 0.552632, 0.439024), \
                                                             np.where(yesterday_price_volumn, 0.282051, 0.608696)), \
                                                     np.where(yesterday_price_change, \
                                                             np.where(yesterday_price_volumn, 0.62037, 0.417323), \
                                                             np.where(yesterday_price_volumn, 0.425926, 0.621622))), \
                                            np.where(month_average_volumn, \
                                                     np.where(yesterday_price_change, \
                                                             np.where(yesterday_price_volumn, 0.561798, 0.5), \
                                                             np.where(yesterday_price_volumn, 0.456522, 0.62963)), \
                                                     np.where(yesterday_price_change, \
                                                             np.where(yesterday_price_volumn, 0.462963, 0.461538), \
                                                             np.where(yesterday_price_volumn, 0.492537, 0.56338)))))

today_price_change = pymc.Bernoulli('today_price_change', p_today_price_change, value=np.ones(len(observed_values)))

model = pymc.Model([today_price_change, p_today_price_change, \
                    yesterday_price_volumn, p_yesterday_price_volumn, yesterday_price_change, p_yesterday_price_change, \
                    month_average_volumn, p_month_average_volumn, month_average_price, p_month_average_price, \
                    sales, p_sales, \
                    new_product_release, negative_news, S_and_P_500, Nasdaq])

mcmc = pymc.MCMC(model)
mcmc.sample(110000, 10000)

trace_new_product_release = mcmc.trace('new_product_release')[:]
trace_negative_news = mcmc.trace('negative_news')[:]
trace_S_and_P_500 = mcmc.trace('S_and_P_500')[:]
trace_Nasdaq = mcmc.trace('Nasdaq')[:]
trace_sales = mcmc.trace('sales')[:]
trace_p_sales = mcmc.trace('p_sales')[:]
trace_month_average_price = mcmc.trace('month_average_price')[:]
trace_p_month_average_price = mcmc.trace('p_month_average_price')[:]
trace_month_average_volumn = mcmc.trace('month_average_volumn')[:]
trace_p_month_average_volumn = mcmc.trace('p_month_average_volumn')[:]
trace_yesterday_price_change = mcmc.trace('yesterday_price_change')[:]
trace_p_yesterday_price_change = mcmc.trace('p_yesterday_price_change')[:]
trace_yesterday_price_volumn = mcmc.trace('yesterday_price_volumn')[:]
trace_p_yesterday_price_volumn = mcmc.trace('p_yesterday_price_volumn')[:]
trace_today_price_change = mcmc.trace('today_price_change')[:]
trace_p_today_price_change = mcmc.trace('p_today_price_change')[:]

dictionary = {
                'new_product_release': [1 if ii[0] else 0 for ii in trace_new_product_release.tolist() ],
                'negative_news': [1 if ii[0] else 0 for ii in trace_negative_news.tolist() ],
                'S_and_P_500': [1 if ii[0] else 0 for ii in trace_S_and_P_500.tolist() ],
                'Nasdaq': [1 if ii[0] else 0 for ii in trace_Nasdaq.tolist() ],
                'sales': [1 if ii[0] else 0 for ii in trace_sales.tolist() ],
                'sales probability':  [ii[0] for ii in trace_p_sales.tolist()],
                'month_average_price': [1 if ii[0] else 0 for ii in trace_month_average_price.tolist() ],
                'month_average_price probability':  [ii[0] for ii in trace_p_month_average_price.tolist()],
                'month_average_volumn': [1 if ii[0] else 0 for ii in trace_month_average_volumn.tolist() ],
                'month_average_volumn probability':  [ii[0] for ii in trace_p_month_average_volumn.tolist()],
                'yesterday_price_change': [1 if ii[0] else 0 for ii in trace_yesterday_price_change.tolist() ],
                'yesterday_price_change probability':  [ii[0] for ii in trace_p_yesterday_price_change.tolist()],
                'yesterday_price_volumn': [1 if ii[0] else 0 for ii in trace_yesterday_price_volumn.tolist() ],
                'yesterday_price_volumn probability':  [ii[0] for ii in trace_p_yesterday_price_volumn.tolist()],
                'today_price_change': [1 if ii[0] else 0 for ii in trace_today_price_change.tolist()],
                'today_price_change probability': [ii[0] for ii in trace_p_today_price_change.tolist()],
              }
df = pd.DataFrame(dictionary)
df.head(20)

p_day1 = float(df[(df['new_product_release'] == 0) & (df['negative_news'] == 0) & (df['sales'] == 1) & \
                  (df['month_average_price'] == 1) & (df['month_average_volumn'] == 1) & (df['S_and_P_500'] == 0) & \
                  (df['Nasdaq'] == 0) & (df['yesterday_price_change'] == 0) & (df['yesterday_price_volumn'] == 1) & \
                  (df['today_price_change'] == 1)].shape[0]) \
                / df[(df['new_product_release'] == 0) & (df['negative_news'] == 0) & (df['sales'] == 1) & \
                  (df['month_average_price'] == 1) & (df['month_average_volumn'] == 1) & (df['S_and_P_500'] == 0) & \
                  (df['Nasdaq'] == 0) & (df['yesterday_price_change'] == 0) & (df['yesterday_price_volumn'] == 1)].shape[0] 
print(p_day1)
