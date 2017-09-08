# generic-csv-2-flare
Easy, automated method to convert csv files to hierarchical json files for use with d3 in the flare format. 

# how to use
First, have a table. Here's a generic one. 

| Method  | Methods to Capture Endpoints  | Therapeutic Area | Target  | Comorbidities  | Known Affects | Reference  | Data  | Functionality |
|---------|-------------------------------|------------------|---------|----------------|---------------|------------|-------|---------------|
| Method1 | Methods to Capture Endpoints1 | Area1            | Target1 | Comorbidities1 | Affects1      | Reference1 | Data1 | Func1         |
| Method1 | Methods to Capture Endpoints1 | Area1            | Target1 | Comorbidities1 | Affects1      | Reference1 | Data1 | Func2         |
| Method2 | Methods to Capture Endpoints1 | Area1            | Target1 | Comorbidities1 | Affects1      | Reference1 | Data1 | Func1         |
| Method2 | Methods to Capture Endpoints2 | Area2            | Target2 | Comorbidities2 | Affects2      | Reference2 | Data2 | Func2         |

First define the grouping order for your dataset. Don't worry, you can remove columns you don't want. Just hardcode the order. 
```
grouping_order = ['Method',
                  'Methods to Capture Endpoints',
                  'Therapeutic Area',
                  'Target',
                  'Comorbidities',
                  'Known Affects',
                  'Reference',
                  'Data',
                  'Functionality'
                  ]
```

Then run. The output makes a json. Go back and change the grouping order to re-arrange and re-group the table. 

Works with python 2 or 3. 
