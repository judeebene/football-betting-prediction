function [statMatrix,listMatrix,dateMatrix,matchList]=readCSV(filePath)

    importedCSV=importdata(filePath);
    
    tempMatchList=importedCSV.textdata(:,2);
    matchList=importedCSV.textdata(:,2:3);
    listMatrix=unique(tempMatchList);
    statMatrix=importedCSV.data;
    dateMatrix=importedCSV.textdata(:,1);

end