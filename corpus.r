library(arrow)
library(dplyr)

library(HunMineR)
library(readtext)
library(lubridate)
library(stringr)
library(ggplot2)
library(quanteda)
library(quanteda.textstats)
library(quanteda.textplots)
library(GGally)
library(ggdendro)
library(tidytext)
library(plotly)


ujsag_data <- read_parquet("./texts/text_as_data/teljes_ujsag_text.parquet")
View(ujsag_data)
custom_stopwords <- HunMineR::data_stopwords_extra

#i will demonstrate the text data of the news outlets on the subset of telex and the previous categorization of text_contains. 
#Text contains is a variable that gets TRUE value when the text of the article contains one of the search words previously used in the data generating process.
corpus_telex_relevant <- ujsag_data %>% filter(ujsag == "telex") %>% filter(text_contains == TRUE)
corpus_telex <- corpus(corpus_telex_relevant$text)
corpus_origo_relevant <- ujsag_data %>% filter(ujsag == "origo") %>% filter(text_contains == TRUE)
corpus_origo <- corpus(corpus_origo_relevant$text)
corpus_24hu_relevant <- ujsag_data %>% filter(ujsag == "24.hu") %>% filter(text_contains == TRUE)
corpus_24hu <- corpus(corpus_24hu_relevant$text)

summary(corpus_telex)


corpus_telex %>%
  tokens() %>%
  tokens_select(pattern = custom_stopwords, selection = "remove") %>%
  tokens_select(pattern = c("másolás"), selection = "remove") %>% 
  textstat_collocations(
    size = 2,
    min_count = 6
  ) %>%
  head(n = 10)

corpus_24hu %>%
  tokens() %>%
  tokens_select(pattern = custom_stopwords, selection = "remove") %>%
  tokens_select(pattern = c("másolás"), selection = "remove") %>% 
  textstat_collocations(
    size = 2,
    min_count = 6
  ) %>%
  head(n = 10)

corpus_origo %>%
  tokens() %>%
  tokens_select(pattern = custom_stopwords, selection = "remove") %>%
  tokens_select(pattern = c("másolás"), selection = "remove") %>% 
  textstat_collocations(
    size = 2,
    min_count = 6
  ) %>%
  head(n = 10)


corpus_24hu_2 <- corpus_24hu %>% 
  tokens(remove_punct = TRUE) %>% 
  tokens_select(pattern = custom_stopwords, selection = "remove") %>% 
  tokens_select(pattern = c("másolás"), selection = "remove")

hu24_dfm <- dfm(corpus_24hu_2)
hu24_dfm <- dfm_trim(hu24_dfm, min_termfreq = 500)


corpus_telex_2 <- corpus_telex %>% 
  tokens(remove_punct = TRUE) %>% 
  tokens_select(pattern = custom_stopwords, selection = "remove") %>% 
  tokens_select(pattern = c("másolás"), selection = "remove")

telex_dfm <- dfm(corpus_telex_2)
telex_dfm <- dfm_trim(telex_dfm, min_termfreq = 500)

corpus_origo_2 <- corpus_origo %>% 
  tokens(remove_punct = TRUE) %>% 
  tokens_select(pattern = custom_stopwords, selection = "remove") %>% 
  tokens_select(pattern = c("másolás"), selection = "remove")

origo_dfm <- dfm(corpus_origo_2)
origo_dfm <- dfm_trim(origo_dfm, min_termfreq = 500)

textplot_wordcloud(hu24_dfm, min_count = 1000, color = "red")
textplot_wordcloud(telex_dfm, min_count = 1000, color = "red")
textplot_wordcloud(origo_dfm, min_count = 1000, color = "red")
#have to still remove - politika, közölte, írta, beszélt, ráadásul...

######################Innentől az MZP beszédeket nézzük########################x
rm(list = ls())
beszed_data <- read_parquet("./texts/text_as_data/fifty_percent_mzp_speech_data.parquet")
custom_stopwords <- HunMineR::data_stopwords_extra

corpus_mzp <- corpus(beszed_data$text)


corpus_mzp %>%
  tokens() %>%
  tokens_select(pattern = custom_stopwords, selection = "remove") %>%
  tokens_select(pattern = c("másolás"), selection = "remove") %>% 
  textstat_collocations(
    size = 3,
    min_count = 6
  ) %>%
  head(n = 10)

tokens_mzp <- corpus_mzp %>% 
  tokens(remove_punct = TRUE) %>% 
  tokens_select(pattern = custom_stopwords, selection = "remove")


mzp_dfm <- dfm(tokens_mzp)
mzp_dfm <- dfm_trim(mzp_dfm, min_termfreq = 25)
textplot_wordcloud(mzp_dfm, min_count = 50, color = "red")

