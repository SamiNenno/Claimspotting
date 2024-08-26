# Telegram Channel Monitoring

This repository contains a collection of Python scripts designed to monitor and analyze Telegram channels using the Pyrogram library. The data collected is stored in a MongoDB database. This project aims to provide detailed insights into the activity and engagement of various Telegram channels, most of which have been fact-checked by a German fact-checking organization.

## Key Features

- **Fact-Checked Channels**: Most channels monitored have been fact-checked at least once, many underwent multiple checks. In other words, these channels are known to spread misinformation. Some channels are specifically recommended by fact-checkers.
  
- **Data Collection Schedule**: 
  - Channels are accessed every two hours during daytime (6am to 10pm).
  - The 100 most recent posts, along with their metadata, are collected during each access.
  - Nighttime (10pm to 6am) scraping is avoided due to reduced posting activity and limited computational resources (see table below).

- **User Reactions Tracking**: 
  - Reactions such as forwards, views, and emojis are continuously tracked. This alows to track both absolute numbers and growth rates.
  - The number of forwards typically increases up to 44 hours after a post is published, with an average increase observed around 11 hours post-publication.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SamiNenno/Tele_Crawler.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Tele_Crawler
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Activity May 2024

| channel                          |   posts_10pm_to_8am |   posts_8am_to_10pm |   mean_posts_per_hour |   median_posts_per_hour |   mean_forwarding_activity_in_hours |   median_forwarding_activity_in_hours |
|:---------------------------------|--------------------:|--------------------:|----------------------:|------------------------:|------------------------------------:|--------------------------------------:|
| BaerbockLeaks                    |                  13 |                  46 |                   1.4 |                     1   |                                 3.1 |                                   1   |
| imnotbozhena                     |                   0 |                 731 |                   2.2 |                     1   |                                19.6 |                                  10   |
| PatriotSandra                    |                 310 |                 369 |                   4.3 |                     4   |                                 2.3 |                                   1   |
| warhistoryalconafter             |                1043 |                3961 |                   7.2 |                     6   |                                 4.9 |                                   2   |
| slavaded1337                     |                 385 |                1966 |                   4.4 |                     4   |                                 8.1 |                                   5   |
| generalsvr                       |                   0 |                  66 |                   1.1 |                     1   |                                27.6 |                                  25   |
| Wissen_ist_Macht_Archiv_Sammlung |                  77 |                 213 |                   2.9 |                     1   |                                 2.3 |                                   1   |
| reitschusterde                   |                  51 |                 196 |                   1.3 |                     1   |                                27.6 |                                  25.5 |
| ti_origin                        |                   6 |                   5 |                   1.1 |                     1   |                                35   |                                  13   |
| pboehringer                      |                  23 |                  51 |                   1.2 |                     1   |                                16.2 |                                  11   |
| prchand                          |                 181 |                 333 |                   2.1 |                     2   |                                11.9 |                                   8   |
| gelbwesten_chemnitz_erzgebirge   |                  21 |                 166 |                   1.5 |                     1   |                                 7.8 |                                   1   |
| svinkavobmoroke                  |                   0 |                  10 |                   2.5 |                     2.5 |                                29   |                                   9.5 |
| BifFidU                          |                 449 |                1406 |                   8.8 |                     7   |                                 3.5 |                                   1   |
| lutzbachmann                     |                  67 |                 479 |                   2.3 |                     2   |                                 7.2 |                                   5   |
| MartinRutter                     |                  62 |                 440 |                   1.4 |                     1   |                                 9.6 |                                   7   |
| michael_hauke                    |                   2 |                  94 |                   1.7 |                     1   |                                 6.2 |                                   4   |
| CottbusWiderstand                |                  61 |                 176 |                   1.6 |                     1   |                                19.9 |                                  10   |
| nailyaaskerzade                  |                   0 |                  69 |                   1.3 |                     1   |                                 3.5 |                                   2   |
| bjoernbanane                     |                   6 |                  92 |                   1.2 |                     1   |                                 6.3 |                                   3   |
| Klartext2021Gemeinsam            |                 148 |                1167 |                   5.2 |                     4   |                                16.6 |                                  11   |
| wirmachenauf_de                  |                  12 |                  85 |                   1.8 |                     1   |                                13.3 |                                   9   |
| SALDO_VGA                        |                   1 |                 289 |                   1.7 |                     1   |                                 7.4 |                                   6   |
| ProfHockertz                     |                  40 |                  87 |                   1.8 |                     1   |                                23.8 |                                  10   |
| mariupolrada                     |                  16 |                 631 |                   3.1 |                     2   |                                 3.4 |                                   2   |
| FaktenFriedenFreiheit            |                   7 |                 329 |                   1.5 |                     1   |                                20.1 |                                  10   |
| IsraelEurope                     |                1159 |                4125 |                  26.8 |                    15   |                                 2.3 |                                   1   |
| EvaHermanOffiziell               |                 427 |                2196 |                   7.9 |                     8   |                                10.3 |                                   3   |
| infodefGERMANY                   |                  28 |                 621 |                   1.8 |                     1   |                                10.3 |                                   6   |
| QAnons_Deutschland               |                 193 |                 847 |                   2.8 |                     2   |                                11.6 |                                   3   |
| CheckMateNews                    |                   4 |                 215 |                   1.1 |                     1   |                                22.6 |                                  12.5 |
| nasha_stranaZ                    |                 338 |                 518 |                   1.2 |                     1   |                                 2.3 |                                   1   |
| russlandsdeutsche                |                 125 |                 811 |                   2   |                     2   |                                10.9 |                                   7   |
| videodump1                       |                 273 |                 586 |                   3.1 |                     2   |                                 6.5 |                                   3   |
| nachrichtenportal                |                   0 |                 255 |                   1   |                     1   |                                 8.6 |                                   6   |
| swodki                           |                1551 |                6309 |                  15.3 |                    16   |                                 3.4 |                                   3   |
| koppreport                       |                  44 |                 321 |                   1.7 |                     1   |                                11.9 |                                   7   |
| infantmilitario                  |                 623 |                1730 |                   4.2 |                     4   |                                 8.2 |                                   6   |
| HolgerFischerRA                  |                  84 |                 110 |                   2.4 |                     2   |                                13.9 |                                  11   |
| q_anonymous_kanal_deutschland    |                 919 |                3204 |                  13.2 |                     7   |                                 4.5 |                                   2   |
| multipolar_magazin               |                   0 |                  15 |                   1   |                     1   |                                14.4 |                                  11   |
| RA_Friede                        |                  34 |                  71 |                   1.3 |                     1   |                                15.7 |                                  12   |
| ServusDeutschland                |                   3 |                   5 |                   1.3 |                     1   |                                 6.9 |                                   4.5 |
| Rot_Okt                          |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| wissenistmacht1                  |                  22 |                 135 |                   1.3 |                     1   |                                 7.6 |                                   3   |
| nityatelegram                    |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| svr_general                      |                   2 |                  25 |                   1   |                     1   |                                 2   |                                   1   |
| waltp38                          |                   9 |                 101 |                   1.9 |                     1   |                                 2.6 |                                   1   |
| gemeinsamgegenNWO                |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| topnews_at                       |                  65 |                 690 |                   2.2 |                     2   |                                 6   |                                   3   |
| Koord_shtab                      |                   8 |                 540 |                   4.8 |                     5   |                                 4.3 |                                   3   |
| aerztefueraufklaerungoffiziell   |                  10 |                  60 |                   1.6 |                     1   |                                18.2 |                                  10   |
| bernie006                        |                  14 |                  22 |                   1.2 |                     1   |                                16   |                                  11.5 |
| rogerbeckamp                     |                   0 |                  26 |                   1.1 |                     1   |                                 4.3 |                                   1.5 |
| reliablerecentnews               |                   1 |                 627 |                   1.8 |                     2   |                                 2   |                                   1   |
| aktivistmann                     |                  24 |                 100 |                   2   |                     1   |                                 8.5 |                                   6   |
| OVALmedia                        |                   2 |                  15 |                   1.1 |                     1   |                                21.4 |                                  13   |
| DerNeustartGlobal                |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| mod_russia_en                    |                  31 |                 545 |                   1.8 |                     1   |                                 6   |                                   2   |
| russica2                         |                  49 |                 358 |                   1.4 |                     1   |                                10   |                                   6   |
| xntelegramfuerx                  |                  45 |                 221 |                   2.1 |                     2   |                                 2.4 |                                   1   |
| friedentotal_official            |                   0 |                  13 |                   1.3 |                     1   |                                 5.1 |                                   1   |
| Kampf_fuer_unsere_Zukunft        |                 109 |                 382 |                   2.2 |                     1   |                                14.7 |                                  10   |
| Eike_RSS                         |                   2 |                 220 |                   4.5 |                     4   |                                 1   |                                   1   |
| freiesachsen                     |                  12 |                 155 |                   1.1 |                     1   |                                13.4 |                                   9   |
| OpenUkraine                      |                 412 |                1407 |                   4.4 |                     3   |                                 9.1 |                                   6   |
| virologe_marcus                  |                   0 |                   1 |                   1   |                     1   |                                 2   |                                   2   |
| unserRecht                       |                1000 |                 911 |                   6.9 |                     3   |                                 8.9 |                                   1   |
| OstashkoNews                     |                1616 |                3403 |                   6.9 |                     6   |                                 6   |                                   3   |
| INTO_THE_LIGHT_NEWS              |                  42 |                 306 |                   2.1 |                     2   |                                 4.6 |                                   1   |
| lipca11                          |                 247 |                 904 |                   4.4 |                     3   |                                 2.1 |                                   1   |
| ganzheitsarzt_de_diskussion      |                   2 |                   3 |                   1   |                     1   |                               nan   |                                 nan   |
| FreieMedienTV                    |                  47 |                 364 |                   1.5 |                     1   |                                22   |                                  15   |
| Impfschaden_Corona_Schweiz       |                 274 |                1400 |                  11.2 |                     8   |                                20.1 |                                  10   |
| QPLUSPLUSPLUS                    |                  60 |                  50 |                   4.6 |                     2   |                                39.3 |                                  41   |
| ukr_leaks_esp                    |                  27 |                 780 |                   4.9 |                     3   |                                 3.4 |                                   1   |
| smotri_z                         |                 176 |                1145 |                   2.6 |                     2   |                                 4   |                                   1   |
| concordgroup_official            |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| hackberegini                     |                   1 |                  50 |                   1.7 |                     1   |                                15.8 |                                  12   |
| fufmedia                         |                   5 |                  84 |                   5.2 |                     3   |                                18.1 |                                  10   |
| JensKestner                      |                   3 |                  88 |                   2.9 |                     1   |                                 1.4 |                                   1   |
| AntiSozialismus                  |                  11 |                  93 |                   1.3 |                     1   |                                 3.9 |                                   2   |
| martinsellnerIB                  |                  37 |                 187 |                   1.7 |                     1   |                                10.1 |                                   6   |
| einmal_hin_alles_drin            |                2173 |                6288 |                  15   |                    14   |                                11.8 |                                   9.5 |
| impfkritisch                     |                 635 |                1726 |                   4   |                     3   |                                19.2 |                                  10   |
| friekorps                        |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| demostreamgruppe                 |                  33 |                  59 |                   1.2 |                     1   |                                 2.5 |                                   1   |
| Demotermine                      |                1189 |                1810 |                   4.8 |                     3   |                                 2.9 |                                   1   |
| Freeyourmindkanal                |                  10 |                  17 |                   1.2 |                     1   |                                 4.2 |                                   3   |
| sandrachat                       |                 374 |                 550 |                   3.3 |                     2   |                                 7.9 |                                   1   |
| Ubersicht_Ukraine_Kanal          |                 222 |                 795 |                   2   |                     1   |                                 8.5 |                                   5   |
| antiilluminaten                  |                 232 |                1256 |                   6.2 |                     6   |                                15.1 |                                   9   |
| nworeset                         |                   4 |                   5 |                   1.5 |                     1.5 |                                13   |                                  10   |
| prima_sursa_md                   |                   0 |                  10 |                   1.2 |                     1   |                                 5.2 |                                   2   |
| uncut_news                       |                 382 |                 999 |                   4.5 |                     3   |                                18   |                                  10   |
| RASattelmaier                    |                   0 |                  25 |                   1.1 |                     1   |                                21.8 |                                  18   |
| KlagemauerTV                     |                   2 |                  89 |                   1.2 |                     1   |                                29.2 |                                  16   |
| rian_ru                          |                 956 |                3235 |                   5.9 |                     5   |                                 6.7 |                                   3   |
| FrMaWa                           |                  35 |                 326 |                   1.3 |                     1   |                                17.5 |                                  10   |
| vitaliy_klitschko                |                   2 |                 121 |                   3.5 |                     1   |                                10.5 |                                   1   |
| GWisnewski                       |                  83 |                 662 |                   3.3 |                     3   |                                13.7 |                                   9   |
| SolovievLive                     |                1247 |                4024 |                   8.2 |                     7   |                                 6.2 |                                   3   |
| pankalla                         |                  69 |                 237 |                   1.6 |                     1   |                                 5.5 |                                   2   |
| saraslightfight                  |                  67 |                 458 |                   3.4 |                     2   |                                20.7 |                                  14   |
| veibz                            |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| Qparadise                        |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| mod_russia                       |                 237 |                 938 |                   2.1 |                     1   |                                 6.5 |                                   1   |
| RU_S_INT                         |                   9 |                  14 |                   1.9 |                     1.5 |                                 1   |                                   1   |
| webmland                         |                 147 |                 759 |                   2.5 |                     2   |                                 9.4 |                                   6   |
| dominikstapf                     |                   1 |                   0 |                   1   |                     1   |                                 1   |                                   1   |
| Eva_Herman_Diskussion            |                 154 |                1328 |                   3.3 |                     2   |                                16.1 |                                   6   |
| QUERDENKEN                       |                   0 |                   9 |                   1.1 |                     1   |                                 2.1 |                                   1   |
| stratinfo                        |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| PATRIOTEN24                      |                 315 |                 647 |                   2.6 |                     2   |                                 8.7 |                                   3   |
| polifa_channel                   |                   8 |                 105 |                   1.5 |                     1   |                                 6   |                                   5   |
| geroldbeneder                    |                  76 |                 286 |                   1.6 |                     1   |                                 6.7 |                                   4   |
| BjoernHoeckeAfD                  |                   1 |                  52 |                   1.4 |                     1   |                                19.1 |                                  10   |
| julian_reichelt                  |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| mysiagin                         |                  74 |                 358 |                   2.2 |                     1   |                                 5.3 |                                   3   |
| informnapalm                     |                  30 |                 341 |                   2   |                     1   |                                 9.7 |                                   6   |
| weissesarmband                   |                  48 |                 480 |                   3   |                     2   |                                 4.4 |                                   3   |
| QFSQwantum                       |                 398 |                1422 |                   5   |                     3   |                                10.3 |                                   6   |
| stefanhomburg                    |                  12 |                  44 |                   1.3 |                     1   |                                11.1 |                                   9   |
| rosenbusch                       |                  55 |                 255 |                   1.5 |                     1   |                                25.6 |                                  17   |
| naspravdiinfo                    |                 625 |                1983 |                   4.3 |                     4   |                                 6.4 |                                   3   |
| pflegekrankenhauspersonal        |                  41 |                  61 |                   1.3 |                     1   |                                21.2 |                                   7.5 |
| politische_bildersprueche        |                  20 |                 266 |                   1.1 |                     1   |                                10   |                                   8   |
| QAnonWWG1WGA17                   |                  18 |                 170 |                   2.4 |                     2   |                                13.7 |                                   9   |
| AntiSpiegel                      |                  54 |                 229 |                   1.5 |                     1   |                                13.8 |                                   9.5 |
| karpfsebastian                   |                1316 |                4500 |                   9.5 |                     7   |                                10.7 |                                   6   |
| exsuscitati                      |                  75 |                 254 |                   2   |                     1   |                                 5.4 |                                   2   |
| davebrych_public                 |                 186 |                 673 |                   2.5 |                     2   |                                 8.5 |                                   5   |
| booomaktuell                     |                  61 |                 619 |                   2.6 |                     2   |                                16.6 |                                  11   |
| MeineDNEWS                       |                  81 |                 455 |                   1.3 |                     1   |                                13.6 |                                  10   |
| KenFM_Diskussion                 |                 106 |                 482 |                   2   |                     1   |                                17.8 |                                   9   |
| ukraina_ru                       |                1024 |                3266 |                   6.9 |                     7   |                                 5.2 |                                   2   |
| andriyshTime                     |                 228 |                1085 |                   2.9 |                     2   |                                 4.2 |                                   2   |
| naomiseibt                       |                  46 |                 242 |                   1.9 |                     2   |                                 7.9 |                                   3   |
| RusslandDeutsche                 |                 340 |                1563 |                   4.1 |                     3   |                                15.3 |                                   6   |
| drguidohofmann                   |                  42 |                 108 |                   1.6 |                     1   |                                 4.5 |                                   3   |
| farukfirat                       |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| MFARussia                        |                  50 |                 301 |                   1.7 |                     1   |                                 7   |                                   3   |
| LIONMediaNews                    |                  23 |                 362 |                   2.6 |                     2   |                                27.2 |                                  27   |
| cihoma                           |                   1 |                   6 |                   1   |                     1   |                                 9.6 |                                  10   |
| CoronaTransition                 |                 224 |                 334 |                   2   |                     1   |                                 5.3 |                                   2   |
| AntifaAufklaerung                |                 101 |                 999 |                   3.5 |                     2   |                                 4.6 |                                   2   |
| GardeZ66                         |                  21 |                 244 |                   1.2 |                     1   |                                14.4 |                                  12   |
| Geheimnis_Gesundheit             |                  35 |                  55 |                   3.3 |                     1   |                                10.4 |                                  10   |
| wagner_group_pmc                 |                 353 |                1217 |                   3.4 |                     2   |                                 3.8 |                                   1   |
| ombudsmanrf                      |                   8 |                 120 |                   2.8 |                     1   |                                 4.9 |                                   3   |
| INAKARB                          |                   1 |                  13 |                   1.3 |                     1   |                                24.6 |                                  15.5 |
| FactSheetAustria                 |                   0 |                   2 |                   2   |                     2   |                                 1   |                                   1   |
| GHZFriedrichMaik                 |                 219 |                 749 |                   4.3 |                     3   |                                15.2 |                                   9   |
| MTProxyStar                      |                  32 |                 213 |                   1   |                     1   |                                23.1 |                                  20   |
| unzensiert                       |                  87 |                1031 |                   3.6 |                     3   |                                15   |                                   9   |
| GeheimesWissenDerEliten          |                  31 |                 167 |                   1.2 |                     1   |                                11.6 |                                  10   |
| ignazbearth                      |                 436 |                1100 |                   6   |                     3   |                                 4.4 |                                   2   |
| DIE_WELTWOCHE                    |                  77 |                 205 |                   1.2 |                     1   |                                 4.7 |                                   2   |
| minzdrav_ru                      |                   8 |                 311 |                   2.5 |                     1   |                                11.5 |                                   6   |
| Folgedemplan                     |                 438 |                1487 |                   5.8 |                     5   |                                 7.1 |                                   4   |
| BlackoutNewsDE                   |                   0 |                  92 |                   1   |                     1   |                                 1   |                                   1   |
| impfen_nein_danke                |                1107 |                3920 |                  10.5 |                     9   |                                 3.5 |                                   2   |
| fragunsdochDasOriginal           |                   0 |                   0 |                 nan   |                   nan   |                               nan   |                                 nan   |
| CraziiWorld                      |                 135 |                1135 |                   4.8 |                     3   |                                10.3 |                                   6   |
| Patrioten                        |                 103 |                1006 |                   4   |                     3   |                                 2.1 |                                   1   |
| GerhardPoettler                  |                   3 |                  15 |                   1.1 |                     1   |                                11.6 |                                   9   |
| tichyseinblicknews               |                  26 |                 187 |                   1.6 |                     1   |                                 1   |                                   1   |
| ukr_leaks_italia                 |                  54 |                 512 |                   5.1 |                     5   |                                 4.5 |                                   2   |
| RoyalAllemand                    |                 139 |                 231 |                   1.5 |                     1   |                                 8.1 |                                   4.5 |
| rechtsanwaeltin_beate_bahner     |                  44 |                 464 |                   1.7 |                     1   |                                18.7 |                                  10   |
| rabbitresearch                   |                   6 |                 296 |                   2   |                     2   |                                26.6 |                                  10   |
| QlobalChange                     |                  40 |                  49 |                   1.3 |                     1   |                                42.5 |                                  37   |
| Freiheitsboten_Kreis_Guetersloh  |                 168 |                 564 |                   2.5 |                     2   |                                17.7 |                                   6   |
| MariaVladimirovnaZakharova       |                  18 |                 173 |                   1.5 |                     1   |                                16.9 |                                   9   |
| Kulturstudio                     |                  27 |                 779 |                   2.1 |                     1   |                                 9.9 |                                   6   |
| neuesausrussland                 |                  37 |                 283 |                   2.4 |                     2   |                                25.8 |                                  19   |
| macklemachtgutelaune             |                 166 |                1494 |                   3.8 |                     3   |                                18.8 |                                  15   |
| oliverjanich                     |                 335 |                1168 |                   4.6 |                     3   |                                14   |                                   9   |
| AllesAusserMainstream            |                  73 |                 344 |                   2.2 |                     1   |                                22.1 |                                  15   |
| Eikekanal                        |                  26 |                 164 |                   2.8 |                     2   |                                 1   |                                   1   |
| kurze_Vids                       |                 173 |                1410 |                   5.1 |                     5   |                                16.5 |                                  10   |
| LKNews2                          |                  57 |                 469 |                   1.8 |                     1   |                                10.3 |                                   8   |
| lastoppo                         |                  41 |                 298 |                   1.4 |                     1   |                                10.6 |                                   6   |
| samarqandfvb                     |                 119 |                 568 |                   4.5 |                     4   |                                 4.7 |                                   3   |
| Haintz                           |                 158 |                 395 |                   2.2 |                     2   |                                16.7 |                                  11   |
| dallekanal                       |                 136 |                 712 |                   3.1 |                     2   |                                 4.9 |                                   2   |
| ReinerFuellmich                  |                  51 |                 298 |                   2   |                     1   |                                18.5 |                                  12   |
| auf1tv                           |                  34 |                 279 |                   1.1 |                     1   |                                30.3 |                                  25   |
| anonymousnews_org                |                   9 |                  67 |                   1.3 |                     1   |                                22.2 |                                  13   |
| InfoDefenseGer                   |                   2 |                  76 |                   1.1 |                     1   |                                 3.3 |                                   1   |
| GrapheneAgenda                   |                   0 |                  10 |                   1.1 |                     1   |                                43.9 |                                  10   |
| Dr_Heinrich_Fiechtner            |                  50 |                 204 |                   1.8 |                     1   |                                 6.9 |                                   4   |
| oliverjanichinternational        |                   0 |                   1 |                   1   |                     1   |                                 1   |                                   1   |
| revolutionmaltsev                |                 880 |                2862 |                   7   |                     6   |                                 4.7 |                                   1   |
| DEKurier                         |                   3 |                 199 |                   1.3 |                     1   |                                 7.5 |                                   5   |
| DruschbaFM                       |                  21 |                1550 |                   3.7 |                     3   |                                 5.1 |                                   3   |
| mihazank                         |                   4 |                 227 |                   1.1 |                     1   |                                 2.3 |                                   1   |
| tsargradtv                       |                 557 |                1920 |                   3.8 |                     3   |                                 8   |                                   5   |
| HinterdenKulissen2               |                   2 |                 143 |                   1.9 |                     1   |                                24.8 |                                  16   |
| frieden_rockt_offiziell          |                   4 |                  55 |                   1   |                     1   |                                18.4 |                                  10   |
| otryadkovpaka                    |                 324 |                1401 |                   3.3 |                     3   |                                 6.9 |                                   3   |
| kenjebsen                        |                   1 |                 267 |                   1   |                     1   |                                29.4 |                                  15   |


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

We would like to thank the German fact-checking organization for their support and recommendations.

---