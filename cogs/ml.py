import discord
from discord.ext import commands
import asyncio
from sklearn.linear_model import LinearRegression
import numpy
import joblib

# --Comandos de ML: somar, subtrair, multiplicar, dividir, potencia, raizquadrada

# class Ml(commands.Cog):
    # def __init__(self, bot):
        # self.bot = bot
        
    # Comando: teste
    
    # Dados de entrada
    # @commands.command()
    # async def teste(self, ctx, valor1: float):
        # try:
            # numbers = numpy.array([1, 2, 3, 4]).reshape(-1, 1) # Números negativos e positivos
            # results = numpy.array([1, 2, 3, 4])
        
            # Modelo de regressão linear
            # model = LinearRegression()
            # model.fit(numbers, results)
        
            # Ver os coeficientes
            # coef_angular = model.coef_[0]
            # intercepto = model.intercept_

            # Aprendizado
            # valor_preditivo = numpy.array([[valor1]])
            # prevision_learning = model.predict(valor_preditivo)[0] # Prever aprendizado
        # except Exception as e:

# Registro de cog

# async def setup(bot):
    # await bot.add_cog(Ml(bot))