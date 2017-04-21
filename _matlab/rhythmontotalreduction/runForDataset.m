allFolders = dir('./data');

for j = 1:length(allFolders)
    
    tmpStruct = [];
    
    if allFolders(j).name(1) ~= '.'
        
        fprintf('Folder: %s\n', allFolders(j).name);
        
        foldName = allFolders(j).name;
        
        list = dir(sprintf('./data/%s/*.csv',foldName));
        
        for i = 1:length(list)
            tmpStruct = listedInfoFromFile(foldName, list(i).name, tmpStruct);
        end
        
        eval(sprintf('%s_struct = tmpStruct;',...
            allFolders(j).name));
        
    end
    
end