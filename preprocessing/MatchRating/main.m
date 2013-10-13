function main(filePath)

    [statMatrix,listMatrix,dateMatrix,matchList]=readCSV(filePath);
    [x,y]=size(listMatrix);
    goalDiff=getMatchGoalDiff(listMatrix,statMatrix,dateMatrix,matchList,'18.05.2013','20.05.2013');
    weeklyMatchList=getWeeklyMatchList(matchList,dateMatrix,'18.05.2013','20.05.2013');
    createOutputList(listMatrix,goalDiff,weeklyMatchList);
    disp(goalDiff);    
    

end