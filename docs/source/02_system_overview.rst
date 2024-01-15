.. title:: PVPlant | System Overview

.. include:: globals.inc

.. _system_overview:

###############
System Overview
###############

The PV Plant Tool system overview is illustrated in :numref:`fig_pvplant_tool_scope`.

.. figure:: images/PVPlant_scope.jpg
   :name: fig_pvplant_tool_scope
   :width: 100%
   :alt: PV Plant Tool Scope
   :align: center
   :figwidth: image

   PV Plant Tool Scope

The PVPlant tools accepts information as inputs that is processed through models creating
intermediate data, which in turn is processed through other models to ultimately arrive at Fiscal
Projections, the resulting output data.

Weather Model
=============

The weather model accepts location weather records which are available from various sources, and 
produces time series-weather data that the :term:`PVS` Model can process.


Projected Consumption Costing Model
===================================



PV System Model
===============

The PV system model predicts solar energy output of a PV system, given weather data. The model 
outputs time-series solar energy data, which is made available to the :term:`EMS` Model to process.


Genset Model
============



Energy Storage System Model
===========================


Energy Management System Model
==============================

Fiscal Model
============


.. todo:: 

   Provide a brief description of the rest of the models.
