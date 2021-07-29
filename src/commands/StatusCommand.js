const BaseCommand = require('../utils/structures/BaseCommand');
const puppeteer = require('puppeteer');
var fs = require('fs');
const Discord = require('discord.js');

module.exports = class StatusCommand extends BaseCommand {
  constructor() {
      super('status', 'status', []);
  }

  async run(client, message, args) {
      var fileName = 'axie-infinity-status.png';
      try {
          const stats = fs.statSync(fileName);
          if((new Date() - new Date(stats.ctime)) > 5*60*1000)  {
            createScreenshot(fileName);
          }   
          sendMesage(message, stats.ctime.getMinutes());       
      } catch(err) {
        message.channel.send("Something went wrong sending ")
      }
  }
}

async function sendMesage(message, fileLastUpdated) {
  const file = new Discord.MessageAttachment('axie-infinity-status.png');
  const exampleEmbed = {
    title: 'Axie Infinity Server Status',
    image: {
      url: 'attachment://axie-infinity-status.png',
    },
    description: 'Source from https://axie.zone'
  };
  message.channel.send({ files: [file], embed: exampleEmbed });  
}
  
async function createScreenshot(fileName) {
  var statusUrl = 'https://axie.zone/axie-infinity-server-status';

  (async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({
      width: 720,
      height: 1080
    })
  
    process.on('unhandledRejection', (reason, p) => {
      console.error('Unhandled Rejection at: Promise', p, 'reason:', reason);
      browser.close();
    });

    await page.goto(statusUrl, {
      waitUntil: 'networkidle2',
    });

    await page.screenshot(
      { 
        clip: {
          x: 0,
          y: 0,
          width: 500,
          height: 720
        },
        path: fileName
      });
    await browser.close();
  })();
}
