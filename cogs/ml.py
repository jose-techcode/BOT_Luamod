import discord
from discord.ext import commands
import asyncio
from sklearn.linear_model import LinearRegression
import numpy

# --Comandos de ML: soma, subtração, multiplicacaoo, divisao, potencia, radiciacao

class Ml(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Comando: somar
    
    # Dados de entrada
    @commands.command()
    async def somar(self, ctx, valor1: float, valor2: float):
        try:
            numbers = numpy.array([1, 2, 3, 4]).reshape(-1, 1) # Números negativos e positivos
            results = numpy.array([1, 2, 3, 4])
        
            # Modelo de regressão linear
            model = LinearRegression()
            model.fit(numbers, results)
        
            # Ver os coeficientes
            coef_angular = model.coef_[0]
            intercepto = model.intercept_

            # Aprendizado
            valor_preditivo = numpy.array([[valor1 + valor2]])
            prevision_learning = model.predict(valor_preditivo)[0] # Prever aprendizado
            await ctx.send(f"Soma de: {valor1} + {valor2} é igual a: {prevision_learning}") # Começa a partir do vetor 0
        except Exception as e:
            await ctx.send(f"Erro ao somar: {e}")

    # Comando: subtrair

    # Dados de entrada
    @commands.command()
    async def subtrair(self, ctx, valor1: float, valor2: float):
        try:
            numbers = numpy.array([1, 2, 3, 4]).reshape(-1, 1) # Números negativos e positivos
            results = numpy.array([1, 2, 3, 4])
            
            # Modelo de regressão linear
            model = LinearRegression()
            model.fit(numbers, results)
        
            # Ver os coeficientes
            coef_angular = model.coef_[0]
            intercepto = model.intercept_

            # Aprendizado
            value_predict = numpy.array([[valor1 - valor2]])
            prevision_learning = model.predict(value_predict)[0] # Prever aprendizado
            await ctx.send(f"Subtração de: {valor1} - {valor2} é igual a: {prevision_learning}") # Começa a partir do vetor 0
        except Exception as e:
            await ctx.send(f"Erro ao subtrair: {e}")

    # Comando: multiplicar

    # Dados de entrada
    @commands.command()
    async def multiplicar(self, ctx, valor1: float, valor2: float):
        try:
            numbers = numpy.array([1, 2, 3, 4]).reshape(-1, 1) # Números negativos e positivos
            results = numpy.array([1, 2, 3, 4])
            
            # Modelo de regressão linear
            model = LinearRegression()
            model.fit(numbers, results)
        
            # Ver os coeficientes
            coef_angular = model.coef_[0]
            intercepto = model.intercept_

            # Aprendizado
            value_predict = numpy.array([[valor1 * valor2]])
            prevision_learning = model.predict(value_predict)[0] # Prever aprendizado
            await ctx.send(f"Multiplicação de: {valor1} * {valor2} é igual a: {prevision_learning}") # Começa a partir do vetor 0
        except Exception as e:
            await ctx.send(f"Erro ao multiplicar: {e}")

    # Comando: dividir

    # Dados de entrada
    @commands.command()
    async def dividir(self, ctx, valor1: float, valor2: float):
        try:
            numbers = numpy.array([1, 2, 3, 4]).reshape(-1, 1) # Números negativos e positivos
            results = numpy.array([1, 2, 3, 4])
            
            # Modelo de regressão linear
            model = LinearRegression()
            model.fit(numbers, results)
        
            # Ver os coeficientes
            coef_angular = model.coef_[0]
            intercepto = model.intercept_

            # Aprendizado
            value_predict = numpy.array([[valor1 / valor2]])
            prevision_learning = model.predict(value_predict)[0] # Prever aprendizado
            await ctx.send(f"Divisão de: {valor1} / {valor2} é igual a: {prevision_learning}") # Começa a partir do vetor 0
        except Exception as e:
            await ctx.send(f"Erro ao dividir: {e}")

    # Comando: potencia

    # Dados de entrada
    @commands.command()
    async def potencia(self, ctx, valor1: float, valor2: float):
        try:
            numbers = numpy.array([1, 2, 3, 4]).reshape(-1, 1) # Números negativos e positivos
            results = numpy.array([1, 2, 3, 4])
            
            # Modelo de regressão linear
            model = LinearRegression()
            model.fit(numbers, results)
        
            # Ver os coeficientes
            coef_angular = model.coef_[0]
            intercepto = model.intercept_

            # Aprendizado
            value_predict = numpy.array([[valor1 ** valor2]])
            prevision_learning = model.predict(value_predict)[0] # Prever aprendizado
            await ctx.send(f"Potência de: {valor1} elevado ao expoente {valor2} é igual a: {prevision_learning}") # Começa a partir do vetor 0
        except Exception as e:
            await ctx.send(f"Erro ao fazer a potência: {e}")

    # Comando: raiz quadrada

    # Dados de entrada
    @commands.command()
    async def raizquadrada(self, ctx, valor1: float):
        try:
            numbers = numpy.array([1, 2, 3, 4]).reshape(-1, 1) # Números negativos e positivos
            results = numpy.array([1, 2, 3, 4])
            
            # Modelo de regressão linear
            model = LinearRegression()
            model.fit(numbers, results)
        
            # Ver os coeficientes
            coef_angular = model.coef_[0]
            intercepto = model.intercept_

            # Aprendizado
            value_predict = numpy.array([[valor1 ** 0.5]])
            prevision_learning = model.predict(value_predict)[0] # Prever aprendizado
            await ctx.send(f"Raiz quadrada de: {valor1} é igual a: {prevision_learning}") # Começa a partir do vetor 0
        except Exception as e:
            await ctx.send(f"Erro ao obter a raiz: {e}")

# Registro de cog

async def setup(bot):
    await bot.add_cog(Ml(bot))