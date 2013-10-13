function [weeklyMatchList]=getWeeklyMatchList(matchList,dateMatrix,matchPeriodStart,matchPeriodFinish)

[x,y]=size(matchList);
weeklyMatchList={x,2};
counter=0;
for i=1:x
    
    
      if ((datenum(dateMatrix{i},'dd.mm.yyyy')>=datenum(matchPeriodStart,'dd.mm.yyyy'))&&(datenum(dateMatrix{i},'dd.mm.yyyy')<=datenum(matchPeriodFinish,'dd.mm.yyyy')))
          counter=counter+1;
          weeklyMatchList{counter,1}=matchList{i,1};
          weeklyMatchList{counter,2}=matchList{i,2};
      end
    
    
end

end