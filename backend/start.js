const mqtt = require('mqtt')
require('dotenv').config()

const { Telegraf } = require('telegraf')

async function botTelegram() {
    try {
        const bot = new Telegraf(process.env.TOKEN_TELEGRAM)
        await bot.launch()

        const client = mqtt.connect(process.env.HOST_MQTT, {
            clientId: process.env.MQTT_CLIENT_ID,
            username: process.env.MQTT_USERNAME,
            password: process.env.MQTT_PASSWORD,
            clean: true
        })

        client.on('connect', function () {
            client.subscribe('send', function (err) {
                if (!err) {
                    client.publish('presence', 'Hello mqtt')
                }
            })
        })

        client.on('message', function (topic, message) {
            const msg = JSON.parse(message.toString())
            console.log(msg)
            if (msg.status) {
                bot.telegram.sendMessage(process.env.TELEGRAM_GROUP, 'Alerta!!!!')
            }
        })


    } catch (error) {
        throw error
    }
}

botTelegram()