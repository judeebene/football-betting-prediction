function createOutputList(listMatrix,goalDiff,weeklyMatchList)

[x,y]=size(weeklyMatchList);
predictionMatrix=[];
for i=1:x
    
    homeTeamName=weeklyMatchList(i,1);
    h=find(strcmp(listMatrix,homeTeamName)==1);
    homeTeamScore=goalDiff(h);
    awayTeamName=weeklyMatchList(i,2);
    h=find(strcmp(listMatrix,awayTeamName)==1);
    awayTeamScore=goalDiff(h);
    matchRate{i,1}=homeTeamScore-awayTeamScore;
    if (matchRate{i})>8
        predictionMatrix{i,1}='H';
    elseif (matchRate{i})<-8
        predictionMatrix{i,1}='A';
    else
        predictionMatrix{i,1}='D';
    end
    
end

filename = 'matchData.csv';
fid = fopen(filename, 'w');
for row=1:x
    
finalArray{row,1}=weeklyMatchList{row,1};
finalArray{row,2}=weeklyMatchList{row,2};
finalArray{row,3}=predictionMatrix{row,1};
finalArray{row,4}=matchRate{row,1};



fprintf(fid, '%s;%s;%s;%d\n', finalArray{row,:});
end
fclose(fid);


end