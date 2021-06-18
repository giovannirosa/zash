# Libraries
library(ggplot2)
library(dplyr)

# The dataset is provided in the gapminder library
library(gapminder)
data <- gapminder %>% filter(year=="2007") %>% dplyr::select(-year)

# Most basic bubble plot
ggplot(data, aes(x=gdpPercap, y=lifeExp, size = pop)) +
  geom_point(alpha=0.7)




dc <- c()
ul <- c()
ri <- c()

df = expand.grid(a = dc, b = ul)
df[order(df$a), ]

limit <- 100

for (i in 1:10) {
  for (j in 1:10) {
    dc <- c(dc, i)
    ul <- c(ul, j)
    ri <- c(ri, i*j)
  }
}

print(dc)

df <- data.frame(dc,ul,ri)

ggplot(df, aes(x=dc, y=ul, size = ri)) +
  geom_point(alpha=0.5, color="darkgreen") + 
  theme(
    axis.line = element_line(colour = "black", size = .5, linetype = "solid"),
    axis.ticks.length = unit(.2, "cm"),
    panel.background = element_rect(fill = "white", colour="white"),
    panel.grid.major = element_line(colour = "gray", size = .1)
  ) + 
  scale_y_discrete(limits = 1:10) +
  scale_x_discrete(limits = 1:10) +
  labs(x="Number of Device Class", y="Number of Action", size="SD") +
  scale_color_manual(values = c("8" = "red")) + 
  scale_size_continuous(limits = c(1,100))
  

data %>%
  arrange(desc(pop)) %>%
  mutate(country = factor(country, country)) %>%
  ggplot(aes(x=gdpPercap, y=lifeExp, size=pop, color=continent)) +
  geom_point(alpha=0.5) +
  scale_size(range = c(.1, 24), name="Population (M)")