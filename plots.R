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

for (i in 1:10) {
  for (j in 1:10) {
    dc <- c(dc, i)
    ul <- c(ul, j)
    ri <- c(ri, i*j)
  }
}

df <- data.frame(dc,ul,ri)

ggplot(df, aes(x=dc, y=ul, size = ri)) +
  geom_point(alpha=0.5, color="darkblue") + 
  theme(
    axis.line = element_line(colour = "black", size = .5, linetype = "solid", arrow = grid::arrow(length = unit(0.3, "cm"))),
    axis.ticks.length = unit(.2, "cm"),
    panel.background = element_rect(fill = "white", colour="white"),
    panel.grid.major = element_line(colour = "gray", size = .1)
  ) + 
  scale_y_discrete(limits = 1:10) +
  scale_x_discrete(limits = 1:10) +
  labs(x="Number of Device Class", y="Number of User Level", size="RI")

ggplot(df, aes(x=dc, y=ul, size = ri)) +
  geom_point(alpha=0.5, color="darkgreen") + 
  theme(
    axis.line = element_line(colour = "black", size = .5, linetype = "solid", arrow = grid::arrow(length = unit(0.3, "cm"))),
    axis.ticks.length = unit(.2, "cm"),
    panel.background = element_rect(fill = "white", colour="white"),
    panel.grid.major = element_line(colour = "gray", size = .1)
  ) + 
  scale_y_discrete(limits = 1:10) +
  scale_x_discrete(limits = 1:10) +
  labs(x="Number of Device Class", y="Number of Action", size="SD")




  

au <- c()
cd <- c()
pp <- c()

for (i in 1:10) {
  for (j in 1:10) {
    au <- c(au, i)
    cd <- c(cd, j)
    pp <- c(pp, i*j)
  }
}

df <- data.frame(au,cd,pp)


ggplot(df, aes(x=cd, y=au, size = pp)) +
  geom_point(alpha=0.5, color="darkred") + 
  theme(
    axis.line = element_line(colour = "black", size = .5, linetype = "solid", arrow = grid::arrow(length = unit(0.3, "cm"))),
    axis.ticks.length = unit(.2, "cm"),
    panel.background = element_rect(fill = "white", colour="white"),
    panel.grid.major = element_line(colour = "gray", size = .1)
  ) + 
  scale_y_discrete(limits = 1:10) +
  scale_x_discrete(limits = 1:10) +
  labs(x="Number of Critical Devices", y="Number Admin Users", size="PR")