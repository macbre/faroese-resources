#!/usr/bin/env node
// @ts-check
const fsa = require("fs/promises");
const promisify = require("util").promisify;

const logger = require("npmlog");
const nodemw = require("nodemw");
const wikidata = require("nodemw/lib/wikidata");

const client = new nodemw({
  server: "en.wikipedia.org",
  path: "/w",
  //   debug: true,
});

const wikidataClient = new wikidata();

logger.level = "verb";

/**
 * @param {string} category
 * @return {Promise<string[]>}
 */
async function getPagesInCategory(category) {
  return new Promise((resolve, reject) => {
    client.getPagesInCategory(category, (err, pages) => {
      if (err) {
        reject(err);
      } else {
        resolve(
          // return pages from NS_MAIN only
          pages.filter((page) => page.ns === 0).map((page) => page.title)
        );
      }
    });
  });
}

/**
 *
 * @param {string} langCode
 * @return {nodemw}
 */
function getWikipediaByLangCode(langCode) {
  const subdomain = langCode.replace(/wiki$/, "");

  return new nodemw({
    server: `${subdomain}.wikipedia.org`,
    path: "/w",
    // debug: true,
  });
}

/**
 *
 * @param {string} article
 * @param {string} langCode
 * @return {Promise<string>}
 */
async function getArticleInLang(article, langCode) {
  return new Promise((resolve, reject) => {
    const client = getWikipediaByLangCode(langCode);

    client.getArticle(article, (err, wikitext) => {
      if (err) {
        reject(err);
      } else {
        resolve(wikitext);
      }
    });
  });
}

/**
 * @param {string} article
 * @return {Promise<string|null>}
 */
async function getIPA(article) {
  /**
   * An example article: https://no.wikipedia.org/wiki/Nor%C3%B0toftir
   *
   * https://no.wikipedia.org/wiki/Nor%C3%B0toftir?action=edit&veswitched=1 shows:
   *
   * Norwegian: {{IPA2|ˈnoːɹˌtɔftɪɹ}}
   * Swedish:   {{IPA|[ˈnoːɹˌtɔftɪɹ]}}
   * Danish:    {{IPA|ˈnoːʂˌtɔftɪɹ}}
   */
  const languages = ["nowiki", "svwiki", "dewiki"]; // Norwegian, Swedish and Danish Wikipedias are known to have IPA
  const ipaRegEx = /{{IPA2?\|\[?([^\]}]+)\]?}}/g;

  // 1. take the list of articles in other languages
  const links = await wikidataClient.getArticleSitelinks(article);
  // logger.verbose('ipa', `Interwikis found for "${article}": ${Object.keys(links)}`);

  for (const lang of languages) {
    // no expected interwiki found, look further
    if (typeof links[lang] == "undefined") {
      continue;
    }

    const wikitext = await getArticleInLang(links[lang].title, lang);

    // wikitext = '{{IPA2|ˈnoːɹˌtɔftɪɹ}}';
    // /{{IPA2?\|\[?([^\]}]+)\]?}}/g.exec(wikitext);
    const matches = ipaRegEx.exec(wikitext);

    if (!matches) continue;

    logger.verbose("ipa", `Got ${matches} from "${lang}" wiki!`);
    return matches[1];
  }

  return null;
}

/**
 *
 * @param {string} article
 * @return {Promise<Object>}
 */
async function getGeo(article) {
  const GEO_CLAIM = "P625";
  const res = await wikidataClient.getArticleClaims(article);
  const claim = res[GEO_CLAIM];

  if (!claim) return null;

  // e.g. {latitude: 62.248888888889, longitude: -7.1758333333333}
  const geo = claim[0].mainsnak.datavalue.value;

  // format for the meta tag, e.g.
  // <meta name=”geo.position” content="61.548056, -6.772222">
  const metaTag = `${Number(geo.latitude).toFixed(4)}, ${Number(
    geo.longitude
  ).toFixed(4)}`;
  logger.verbose("geo", `Location for ${article} is: ${metaTag}`);

  return {
    latitude: geo.latitude,
    longitude: geo.longitude,
    metaTag,
  };
}

async function main() {
  // @see https://en.wikipedia.org/wiki/Category:Populated_places_in_the_Faroe_Islands
  const CATEGORY = "Populated places in the Faroe Islands";

  logger.info(
    "villages",
    `Collecting villages articles from '${CATEGORY}' category...`
  );

  const articles = await getPagesInCategory(CATEGORY); // console.log(articles);
  //   const articles = ['Norðtoftir'];
  logger.info("villages", `Pages to process: ${articles.length}`);

  // prepare the results
  const results = {
    villages: [],
  };

  logger.enableProgress();
  logger.info("villages", "Fetching data");

  let idx = 0;
  for (const article of articles) {
    // https://github.com/npm/npmlog/blob/main/lib/log.js#L157
    logger.showProgress(article, idx++ / articles.length);

    results.villages.push({
      name: article,
      ipa: await getIPA(article),
      geo: await getGeo(article),
    });
  }
  logger.disableProgress();

  // save the results
  const filename = __dirname + "/villages.json";

  logger.info("villages", `Saving the results to ${filename} ...`);
  await fsa.writeFile(filename, JSON.stringify(results, null, 2 /* space */));
  logger.info("villages", "Done");
}

(async () => {
  await main();
})();
